# Backend Monitoring & Search Tool

A Python-based CLI tool for scanning large backend data files (logs, database exports, error files, code files) and searching, filtering, and highlighting matching keywords for monitoring and debugging purposes.

## Features

- **File Support**: Scans .log, .txt, .sql, .json, .csv, .py files
- **Search Modes**: Single file or entire directory (recursive)
- **Search Options**: Case-insensitive, partial/full word matching
- **Output**: Displays file name, line number, matched content with highlighted keywords
- **CLI Interface**: Easy-to-use command-line interface
- **Cross-Platform**: Runs on Windows, Linux, Mac, and GitHub Codespaces

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/rounakraj2002/monitoring.git
   cd monitoring/backend-monitor
   ```

2. Install dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool using:

```bash
python monitor.py <path> <keyword> [options]
```

### Arguments

- `path`: Path to file or directory to scan
- `keyword`: Keyword to search for

### Options

- `--file-type EXT`: Filter by file extension (e.g., .log, .sql)
- `--ignore-case`: Case-insensitive search (default)
- `--context-lines N`: Number of context lines around matches
- `--regex`: Treat keyword as regex pattern
- `--export FILE`: Export results to file (txt or csv)

### Examples

1. Search for "error" in a log file:
   ```bash
   python monitor.py sample_data/app.log error
   ```

2. Search for "truncate" in all SQL files in a directory:
   ```bash
   python monitor.py sample_data truncate --file-type .sql
   ```

3. Case-insensitive search for "exception":
   ```bash
   python monitor.py /path/to/directory exception --ignore-case
   ```

4. Regex search:
   ```bash
   python monitor.py sample_data/app.log "ERROR|WARN" --regex
   ```

## Sample Output

Searching for "truncate":

```
[db_dump.sql:5] TRUNCATE TABLE orders;
[app.log:6] Database **truncate** operation detected
```

Total matches found: 2

## Project Structure

```
backend-monitor/
│
├── monitor.py                 # Main CLI script (single file with all functionality)
├── sample_data/
│ ├── app.log                 # Sample log file
│ ├── db_dump.sql             # Sample database dump
│
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Requirements

- Python 3.10+
- No external dependencies (uses standard library)

## Running in GitHub Codespaces

1. Open the repository in GitHub Codespaces
2. Navigate to the backend-monitor directory
3. Run the commands as shown in the Usage section

## Contributing

Feel free to submit issues and pull requests.

## License

MIT License