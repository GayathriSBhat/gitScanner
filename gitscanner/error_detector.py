import re, base64

# Filenames commonly used to store secrets or credentials
SENSITIVE_FILENAMES = [
    ".env", ".env.local", ".env.production", ".env.development",
    "id_rsa", "id_dsa", "id_ed25519",
    "secrets.yml", "secrets.yaml",
    "config.json", "config.yaml", "config.yml",
    "credentials.json", "firebase.json",
    "aws_credentials", "gcp_key.json",
    ".npmrc", ".netrc", ".pypirc", ".dockercfg",
    ".pem", ".ppk",
]

# File extensions often associated with private keys or certificates
SENSITIVE_SUFFIXES = [".pem", ".ppk", ".key", ".crt", ".p12", ".keystore", ".pkcs12"]

# Regex patterns to detect common secret formats (best-effort scanning)
SECRET_REGEXES = [
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS Access Key ID"),
    (re.compile(r"ASIA[0-9A-Z]{16}"), "AWS Temporary Key ID"),
    (re.compile(r"(?i)aws_secret_access_key\s*[:=]\s*([A-Za-z0-9/+=]{40})"), "AWS Secret Access Key"),
    (re.compile(r"ghp_[A-Za-z0-9]{36}"), "GitHub Personal Access Token"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}-[A-Za-z0-9-]{10,}-[A-Za-z0-9-]{10,}"), "Slack Token"),
    (re.compile(r"AIza[0-9A-Za-z\-_]{35}"), "Google API Key"),
    (re.compile(r"sk_live_[0-9a-zA-Z]{24,}"), "Stripe Live Secret Key"),
    (re.compile(r"sk_test_[0-9a-zA-Z]{24,}"), "Stripe Test Secret Key"),
    (re.compile(r"(?i)password\s*[:=]\s*[^\s]{6,}"), "Password Assignment"),
]

# Extensions typically representing plaintext / readable files
TEXTUAL_EXTS = [
    ".txt",".md",".json",".yaml",".yml",".py",".js",".ts",".java",".go",".rb",".php",
    ".c",".cpp",".rs",".ini",".cfg",".toml",".env"
]

def is_sensitive_name(path):
    """Check if file name is known to contain secrets or uses a sensitive suffix."""
    name = path.split("/")[-1]  # Extract the filename only

    # Exact filename match
    if name in SENSITIVE_FILENAMES:
        return True

    # Suffix match (e.g. .pem, .key)
    for s in SENSITIVE_SUFFIXES:
        if name.endswith(s):
            return True

    return False

def is_textual(path):
    """Return True if file looks like text based on extension."""
    path_lower = path.lower()
    return any(path_lower.endswith(ext) for ext in TEXTUAL_EXTS)

def decode_content(item):
    """Decode base64-encoded file content safely. Return None on failure."""
    if not item or item.get("encoding") != "base64":
        return None
    try:
        return base64.b64decode(item["content"]).decode("utf-8", errors="replace")
    except Exception:
        return None  # If decoding fails, skip silently

def find_secrets(text, max_matches=3):
    """
    Search text for secret patterns based on SECRET_REGEXES.
    Returns up to 'max_matches' potential secret findings with small context snippets.
    """
    matches = []
    for rx, label in SECRET_REGEXES:
        for m in rx.finditer(text or ""):
            # Include a snippet of text around the match for context
            snippet = text[max(0, m.start()-20):m.end()+20]
            matches.append({
                "type": label,
                "snippet": snippet.strip()
            })

            # Stop early once threshold reached
            if len(matches) >= max_matches:
                return matches

    return matches

def severity_for(issues):
    """
    Assign severity score based on detected issues.
    Priority order:
    - Exposed secrets or sensitive files → High
    - Missing metadata → Low
    - Otherwise → None
    """
    if "Exposed Secrets" in issues:
        return "High"
    if "Sensitive Files" in issues:
        return "High"
    if "Missing Metadata" in issues:
        return "Low"
    return "None"
