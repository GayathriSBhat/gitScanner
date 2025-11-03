

# GitScanner

## References

Github API
https://docs.github.com/en/rest/using-the-rest-api/getting-started-with-the-rest-api?apiVersion=2022-11-28

Request Rate Limit
https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api?apiVersion=2022-11-28


CLI Output in Tabular Format:
https://rich.readthedocs.io/en/latest/tables.html#



# How to run cli app? 

python3 -m gitScannerApp --user octocat --token "$GITHUB_TOKEN"  --max-files 75

# How to run web dashboard?

python3 -m gitScannerApp.router


# Output Screenshots

<img width="441" height="223" alt="Screenshot from 2025-11-03 18-27-29" src="https://github.com/user-attachments/assets/fd578eed-2dbb-4992-a836-031ec54418a1" />
