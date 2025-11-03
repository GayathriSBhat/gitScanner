import requests

BASE = "https://api.github.com"

def _headers(token):
    """
    Build HTTP headers for GitHub API requests.
    Includes authorization if a token is provided.
    """
    h = {"Accept": "application/vnd.github+json", "User-Agent": "metron-scanner"}
    # print("Token present?", bool(token))
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h

def list_repos(target, mode="user", token=None, timeout=5.0):
    """
    List all repositories for a GitHub user or organization.
    
    Parameters:
        target (str): GitHub username or organization name.
        mode (str): "user" for users, "org" for organizations.
        token (str): Optional GitHub API token for authentication.
        timeout (float): Request timeout in seconds.
        
    Returns:
        list: List of repository objects from GitHub API.
    """
    # Choose correct endpoint based on mode
    url = f"{BASE}/users/{target}/repos" if mode == "user" else f"{BASE}/orgs/{target}/repos"
    
    repos = []
    page = 1
    
    # Paginate until no more repos are returned
    while True:
        r = requests.get(
            url,
            headers=_headers(token),
            params={"per_page": 100, "page": page},
            timeout=timeout
        )
        r.raise_for_status()
        batch = r.json()
        #print(batch)
        
        if not batch:
            break
        
        repos.extend(batch)
        page += 1
    
    return repos

def get_repo(target, name, token=None, timeout=5.0):
    """
    Get metadata for a specific GitHub repository.
    
    Parameters:
        target (str): GitHub username or organization.
        name (str): Repository name.
        token (str): Optional GitHub API token.
        timeout (float): Request timeout.
    
    Returns:
        dict: Repository metadata.
    """
    url = f"{BASE}/repos/{target}/{name}"
    r = requests.get(url, headers=_headers(token), timeout=timeout)
    r.raise_for_status()
    # print(r.json)
    return r.json()

def get_tree(target, name, sha, token=None, timeout=5.0):
    """
    Retrieve the Git tree for a repository (optionally recursive).
    
    Parameters:
        target (str): Owner of the repository.
        name (str): Repository name.
        sha (str): SHA hash of the commit/tree to retrieve.
        token (str): Optional GitHub API token.
        timeout (float): Request timeout.
        
    Returns:
        dict: Tree data structure returned by GitHub API.
    """
    url = f"{BASE}/repos/{target}/{name}/git/trees/{sha}"
    r = requests.get(
        url,
        headers=_headers(token),
        params={"recursive": 1},  # Fetch full file tree recursively
        timeout=timeout
    )
    r.raise_for_status()
    # print(r.json)
    return r.json()

def get_file_metadata(target, name, path, token=None, timeout=5.0):
    """
    Get metadata for a specific file in a repository.
    
    Parameters:
        target (str): Owner of the repo.
        name (str): Repository name.
        path (str): Path to file inside repo.
        token (str): Optional GitHub API token.
        timeout (float): Request timeout.
    
    Returns:
        dict or None: File metadata, or None if file not found.
    """
    url = f"{BASE}/repos/{target}/{name}/contents/{path}"
    r = requests.get(url, headers=_headers(token), timeout=timeout)
    
    # Gracefully return None if file does not exist
    if r.status_code == 404:
        return None
    
    r.raise_for_status()
    # print(r.json)
    return r.json()
