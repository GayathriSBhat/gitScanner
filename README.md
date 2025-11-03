# GitScanner

Gitscanner is a  tool to check for exposed API keys, SSH keys and other sensistive data commited 
unintentionally by users or organizations.

It scans through repositories and checks where the error is and reports severity of the same.

Additionally, it also verifies if the repo has a readme and licesne. 

## References

- [Github API Documentation](https://docs.github.com/en/rest/using-the-rest-api/getting-started-with-the-rest-api?apiVersion=2022-11-28)
- [Request Rate Limit Documentation](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api?apiVersion=2022-11-28)
- [CLI Output in Tabular Format](https://rich.readthedocs.io/en/latest/tables.html#)

## CLI Usage

Run the CLI application with:
```bash
python -m gitscanner
```

### Available Options:
| Option | Description |
|--------|-------------|
| `--user` | GitHub username for the repo |
| `--org` | Organization name (if applicable) |
| `--token` | Access token for higher output volume |
| `--timeout` | Maximum request time |
| `--max-files` | Limit number of files processed to increase execution time |
| `--json` | Display output in JSON format |
| `--html` | Render web dashboard |

## Web Dashboard

Run the web dashboard with:
```bash
python3 -m gitscanner.router
```

## Output Screenshots

### CLI Interface
![CLI Output](https://github.com/user-attachments/assets/fd578eed-2dbb-4992-a836-031ec54418a1)

### Web Dashboard
![Web Dashboard](https://github.com/user-attachments/assets/288493bf-d7d9-4d4d-9747-c9cc30494168)