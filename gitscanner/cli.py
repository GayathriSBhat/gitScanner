import argparse, json, sys
from .repo_scanner import scan_account
from .report import print_table, write_html_report

def main():
    # Initialize argument parser for CLI usage
    p = argparse.ArgumentParser(description="GitScanner")

    # Require either --user or --org, but not both
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--user", help="GitHub username to scan")
    g.add_argument("--org", help="GitHub organization to scan")

    # Optional GitHub token to increase rate limits and access private repos
    p.add_argument("--token", help="GitHub token (optional)", default=None)

    # HTTP timeout for each API request
    p.add_argument("--timeout", type=float, default=5.0, help="HTTP timeout per request (s)")

    # Limit to avoid scanning very large repos exhaustively
    p.add_argument("--max-files", type=int, default=1000, help="Max files to inspect per repo")

    # Output options: JSON and HTML report files
    p.add_argument("--json", dest="json_out", help="Write JSON report to this path")
    p.add_argument("--html", dest="html_out", help="Write HTML report to this path")

    # Parse the command-line arguments
    args = p.parse_args()

    # Determine scan target value and mode (user vs org)
    target = args.user or args.org
    mode = "user" if args.user else "org"

    # Run the scanner logic and obtain results
    results = scan_account(
        target,
        mode=mode,
        token=args.token,
        timeout=args.timeout,
        max_files=args.max_files
    )

    # Write results to JSON file if specified
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

    # Write results to HTML report if specified
    if args.html_out:
        write_html_report(results, args.html_out)

    # Display a table summary in the terminal
    print_table(results)

# Entry point when script is executed directly
if __name__ == "__main__":
    main()
