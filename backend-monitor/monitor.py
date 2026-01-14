#!/usr/bin/env python3
"""
Backend Monitoring & Search Tool

A CLI tool for searching and highlighting keywords in backend data files.
Supports log files, database exports, error files, and code files.
"""

import argparse
import re
import sys
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
    supported_extensions = {'.log', '.txt', '.sql', '.json', '.csv', '.py'}

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