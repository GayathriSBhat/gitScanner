# GitScanner

![Dashboard Screenshot](https://github.com/user-attachments/assets/942b8ce8-39d6-477b-9dc9-ae2227f92902)

## References

- [Github API Documentation](https://docs.github.com/en/rest/using-the-rest-api/getting-started-with-the-rest-api?apiVersion=2022-11-28)
- [Request Rate Limit Documentation](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api?apiVersion=2022-11-28)
- [CLI Output in Tabular Format](https://rich.readthedocs.io/en/latest/tables.html#)

## CLI Usage

Run the CLI application with:
```bash
python -m git
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
python3 -m gitScannerApp.router
```

## Output Screenshots

### CLI Interface
![CLI Output](https://github.com/user-attachments/assets/fd578eed-2dbb-4992-a836-031ec54418a1)

### Web Dashboard
![Web Dashboard](https://github.com/user-attachments/assets/288493bf-d7d9-4d4d-9747-c9cc30494168)