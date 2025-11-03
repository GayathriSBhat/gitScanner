from .api_handler import list_repos, get_repo, get_tree, get_file_metadata
from .error_detector import is_sensitive_name, is_textual, decode_content, find_secrets, severity_for

def scan_account(target, mode="user", token=None, timeout=5.0, max_files=1000, max_file_size=200_000):
    """
    Scan a GitHub user/org for risky files, secrets, and missing metadata.

    Parameters:
        target (str): GitHub user or organization
        mode (str): "user" or "org"
        token (str): Optional GitHub token for authenticated requests
        timeout (float): Request timeout per HTTP call
        max_files (int): Max files to examine per repository
        max_file_size (int): Max file size to fetch for secret scanning (bytes)

    Returns:
        dict: Scan results including issues per repository
    """

    # Fetch repo list for target account
    repos = list_repos(target, mode=mode, token=token, timeout=timeout)

    results = {"target": target, "mode": mode, "repos": []}

    for r in repos:
        name = r["name"]

        # Determine default branch name
        default_branch = r.get("default_branch") or "main"

        # Fetch full repo metadata
        repo_meta = get_repo(target, name, token=token, timeout=timeout)

        # GitHub API workaround: get tree via branch ref
        ref = repo_meta["default_branch"]

        # Get full file tree for branch
        tree = get_tree(target, name, f"heads/{ref}", token=token, timeout=timeout)

        # Extract blob (file) entries only, respecting max file scan limit
        files = [t for t in (tree.get("tree") or []) if t.get("type") == "blob"]
        files = files[:max_files]

        # Track issues and details per repo
        issues = set()
        details = {"Sensitive Files": [], "Exposed Secrets": [], "Missing Metadata": []}

        # Check for missing README / LICENSE in repo root files
        root_names = set([f["path"].split("/")[-1] for f in files if "/" not in f["path"]])
        if not any(n.lower().startswith("readme") for n in root_names) or not any("license" in n.lower() for n in root_names):
            issues.add("Missing Metadata")

        # Detect sensitive files based on filename patterns
        for f in files:
            path = f["path"]
            if is_sensitive_name(path):
                issues.add("Sensitive Files")
                details["Sensitive Files"].append({"path": path})

        # Scan textual files for secrets
        for f in files:
            path = f["path"]
            size = f.get("size", 0)

            # Skip very large files
            if size and size > max_file_size:
                continue

            # Only inspect text-like files
            if not is_textual(path):
                continue

            # Fetch file contents
            item = get_file_metadata(target, name, path, token=token, timeout=timeout)
            if not item:
                continue

            # Decode base64 content returned by GitHub API
            text = decode_content(item)
            if not text:
                continue

            # Run secret detection rules
            secret_hits = find_secrets(text)
            if secret_hits:
                issues.add("Exposed Secrets")
                for h in secret_hits:
                    details["Exposed Secrets"].append({"path": path, **h})

        # Compute severity based on detected issue categories
        severity = severity_for(issues) if issues else "None"

        # Add repository results
        results["repos"].append({
            "name": name,
            "issues": sorted(list(issues)),
            "severity": severity,
            "details": details,
            "html_url": r.get("html_url"),
        })

    return results
