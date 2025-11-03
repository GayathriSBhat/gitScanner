# Load environment variables from a .env file
from dotenv import load_dotenv
load_dotenv()

import os, json
from flask import Flask, request, jsonify, render_template_string
from .repo_scanner import scan_account     # Custom module for scanning GitHub account

# Initialize Flask app
app = Flask(__name__)

# API endpoint to trigger a scan and return JSON
@app.route("/api/scan")
def api_scan():
    # Read query params, falling back to environment variables or defaults
    target = request.args.get("target") or os.environ.get("TARGET_USER", "octocat")
    mode = request.args.get("mode") or os.environ.get("MODE", "user")
    token = request.args.get("token") or os.environ.get("GITHUB_TOKEN")
    timeout = float(request.args.get("timeout") or 5.0)
    max_files = int(request.args.get("max_files") or 600)

    # Perform the scan
    results = scan_account(target, mode=mode, token=token, timeout=timeout, max_files=max_files)

    # Return results as JSON
    return jsonify(results)


# Entry point for running the app
def main():
    port = int(os.environ.get("PORT", "5000"))  # Default to port 5000 if not set
    app.run(host="0.0.0.0", port=port)          # Run Flask on all interfaces

# Run app if file is executed directly
if __name__ == "__main__":
    main()
