#!/usr/bin/env python3
"""
Backend Monitoring & Search Tool

A CLI tool for searching and highlighting keywords in backend data files.
Supports log files, database exports, error files, code files, and database files.
"""

import argparse
import re
import sys
import sqlite3
from pathlib import Path


def log_error(message):
    """
    Log an error message to stderr.

    Args:
        message (str): Error message
    """
    print(f"Error: {message}", file=sys.stderr)


def read_file_lines(file_path):
    """
    Read all lines from a file.

    Args:
        file_path (Path): Path to the file

    Returns:
        list: List of lines
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.readlines()


def query_database(db_path, keyword, ignore_case=True, is_regex=False):
    """
    Query a SQLite database for the keyword in all tables and columns.

    Args:
        db_path (Path): Path to the database file
        keyword (str): Keyword to search
        ignore_case (bool): Whether to ignore case
        is_regex (bool): Whether keyword is regex

    Returns:
        list: List of match dictionaries
    """
    matches = []
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table_name, in tables:
            try:
                # Get column names for this table
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]

                # Query all data from this table
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()

                for row_idx, row in enumerate(rows, 1):
                    for col_idx, cell_value in enumerate(row):
                        if cell_value is not None:
                            cell_str = str(cell_value)
                            lines = cell_str.split('\n')  # Handle multi-line content

                            for line_idx, line in enumerate(lines, 1):
                                if is_regex:
                                    pattern = keyword
                                else:
                                    pattern = re.escape(keyword)

                                flags = re.IGNORECASE if ignore_case else 0
                                match = re.search(pattern, line, flags)
                                if match:
                                    matches.append({
                                        'file': str(db_path),
                                        'table': table_name,
                                        'column': column_names[col_idx] if col_idx < len(column_names) else f'col_{col_idx}',
                                        'row': row_idx,
                                        'line': line.rstrip(),
                                        'start': match.start(),
                                        'end': match.end()
                                    })
            except sqlite3.Error as e:
                # Skip tables that can't be queried
                continue

        conn.close()
    except sqlite3.Error as e:
        log_error(f"Database error for {db_path}: {e}")
    except Exception as e:
        log_error(f"Error querying database {db_path}: {e}")

    return matches


def scan_and_search(path, keyword, supported_extensions, file_type_filter=None,
                   ignore_case=True, is_regex=False, context_lines=0):
    """
    Scan the given path (file or directory) and search for the keyword.

    Args:
        path (Path): Path to file or directory
        keyword (str): Keyword to search
        supported_extensions (set): Set of supported file extensions
        file_type_filter (str): Optional file type filter
        ignore_case (bool): Whether to ignore case
        is_regex (bool): Whether keyword is regex
        context_lines (int): Number of context lines

    Returns:
        list: List of match dictionaries with file, line_num, line, start, end
    """
    matches = []

    if path.is_file():
        files_to_scan = [path]
    else:
        files_to_scan = []
        for ext in supported_extensions:
            if file_type_filter and ext != file_type_filter:
                continue
            files_to_scan.extend(path.rglob(f'*{ext}'))

    flags = re.IGNORECASE if ignore_case else 0

    for file_path in files_to_scan:
        try:
            # Handle database files differently
            if file_path.suffix.lower() in ['.db', '.sqlite', '.sqlite3']:
                db_matches = query_database(file_path, keyword, ignore_case, is_regex)
                matches.extend(db_matches)
            else:
                # Handle text files as before
                lines = read_file_lines(file_path)
                for line_num, line in enumerate(lines, 1):
                    if is_regex:
                        pattern = keyword
                    else:
                        pattern = re.escape(keyword)

                    match = re.search(pattern, line, flags)
                    if match:
                        matches.append({
                            'file': str(file_path),
                            'line_num': line_num,
                            'line': line.rstrip(),
                            'start': match.start(),
                            'end': match.end()
                        })
        except Exception as e:
            log_error(f"Error reading {file_path}: {e}")

    return matches


def highlight_matches(matches, keyword, is_regex=False):
    """
    Highlight the keyword in the matched lines using ANSI colors.

    Args:
        matches (list): List of match dicts
        keyword (str): Keyword to highlight
        is_regex (bool): Whether keyword is regex

    Returns:
        list: List of formatted strings with highlights
    """
    highlighted_lines = []
    for match in matches:
        # Handle database matches differently
        if 'table' in match:
            file_name = Path(match['file']).name
            table = match['table']
            column = match['column']
            row = match['row']
            line = match['line']
            start, end = match['start'], match['end']

            # ANSI escape codes for bold red
            highlight_start = '\033[1;31m'
            highlight_end = '\033[0m'

            highlighted_line = f"{highlight_start}{line[start:end]}{highlight_end}"
            full_line = f"[{file_name}:{table}.{column}:row{row}] {line[:start]}{highlighted_line}{line[end:]}"
        else:
            # Handle text file matches
            file_name = Path(match['file']).name
            line = match['line']
            start, end = match['start'], match['end']

            # ANSI escape codes for bold red
            highlight_start = '\033[1;31m'
            highlight_end = '\033[0m'

            highlighted_line = f"{highlight_start}{line[start:end]}{highlight_end}"
            full_line = f"[{file_name}:{match['line_num']}] {line[:start]}{highlighted_line}{line[end:]}"

        highlighted_lines.append(full_line)

    return highlighted_lines


def main():
    parser = argparse.ArgumentParser(
        description="Backend Monitoring & Search Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python monitor.py /path/to/file.log error
  python monitor.py /path/to/directory truncate --file-type .sql
  python monitor.py /path/to/database.db username --file-type .db
  python monitor.py /path/to/file.py exception --ignore-case
        """
    )
    parser.add_argument('path', help='Path to file or directory to scan')
    parser.add_argument('keyword', help='Keyword to search for')
    parser.add_argument('--file-type', help='Filter by file extension (e.g., .log, .sql)')
    parser.add_argument('--ignore-case', action='store_true', default=True, help='Case-insensitive search (default)')
    parser.add_argument('--context-lines', type=int, default=0, help='Number of context lines around matches')
    parser.add_argument('--regex', action='store_true', help='Treat keyword as regex pattern')
    parser.add_argument('--export', help='Export results to file (txt or csv)')

    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        log_error(f"Path does not exist: {path}")
        sys.exit(1)

    # Supported file types
    supported_extensions = {'.log', '.txt', '.sql', '.json', '.csv', '.py', '.db', '.sqlite', '.sqlite3'}

    try:
        matches = scan_and_search(path, args.keyword, supported_extensions, args.file_type,
                                args.ignore_case, args.regex, args.context_lines)

        if matches:
            highlighted = highlight_matches(matches, args.keyword, args.regex)
            for line in highlighted:
                print(line)
            print(f"\nTotal matches found: {len(matches)}")
        else:
            print("No matches found.")

        if args.export:
            # Implement export later if needed
            pass

    except Exception as e:
        log_error(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()