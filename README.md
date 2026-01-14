# Backend Monitoring & Search Tool

A Python-based CLI tool for scanning large backend data files (logs, database exports, error files, code files) and searching, filtering, and highlighting matching keywords for monitoring and debugging purposes.

## 🎯 Project Overview

This tool was developed to address the need for efficient monitoring and debugging of backend systems. It allows developers and system administrators to quickly search through large volumes of log files, database dumps, and other backend data files to identify issues, track operations, and analyze system behavior.

### Key Use Cases
- **Database Operation Tracking**: Monitor INSERT, UPDATE, DELETE, TRUNCATE operations
- **Error Analysis**: Quickly find ERROR, WARN, EXCEPTION entries across multiple files
- **System Monitoring**: Track user activities, performance issues, and system events
- **Debugging**: Search for specific keywords or patterns in code files and logs
- **Compliance Auditing**: Search for security-related events or data access patterns

## 🏗️ Development Process

### Phase 1: Requirements Analysis
- Identified need for fast, efficient searching across multiple file types
- Determined key features: case-insensitive search, regex support, file type filtering
- Established CLI interface for ease of use in terminal environments

### Phase 2: Architecture Design
- **Single Script Design**: Consolidated all functionality into one Python file for simplicity
- **Modular Functions**: Organized code into logical functions (scanning, highlighting, file reading)
- **Error Handling**: Implemented robust error handling for file access and invalid inputs
- **Performance Considerations**: Used efficient file reading and regex matching

### Phase 3: Implementation
- **Core Functionality**: File scanning with recursive directory support
- **Search Engine**: Regex-based pattern matching with case-insensitive options
- **Output Formatting**: ANSI color highlighting for terminal display
- **CLI Interface**: Argument parsing with comprehensive help and examples

### Phase 4: Testing & Validation
- Tested with various file types (.log, .sql, .txt, .json, .csv, .py, .db, .sqlite, .sqlite3)
- Validated case-insensitive and regex search capabilities
- Verified error handling and edge cases
- Performance tested with sample data

## 🔧 How It Works

### Architecture
```
Input (CLI Args) → File Scanner → Pattern Matcher → Result Highlighter → Output
```

1. **Input Processing**: Parses command-line arguments for path, keyword, and options
2. **File Discovery**: Recursively scans directories or processes single files
3. **Content Analysis**: Reads files line-by-line and applies regex pattern matching
4. **Result Processing**: Collects matches with file location and line information
5. **Output Formatting**: Highlights matched keywords using ANSI escape codes

### Technical Details
- **Language**: Python 3.10+ (uses only standard library)
- **Search Algorithm**: Regex-based with re.IGNORECASE for case-insensitive matching
- **File Handling**: Supports UTF-8 encoding with error tolerance
- **Database Support**: Direct SQLite querying for .db, .sqlite, .sqlite3 files
- **Performance**: Memory-efficient line-by-line processing for large files
- **Output**: Terminal-friendly with color highlighting

## 🚀 Installation & Setup

### Local Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/rounakraj2002/monitoring.git
   cd monitoring/backend-monitor
   ```

2. **Verify Python version**:
   ```bash
   python --version  # Should be 3.10 or higher
   ```

3. **Install dependencies** (if any):
   ```bash
   pip install -r requirements.txt
   ```

### GitHub Codespaces Setup
1. Open the repository in GitHub Codespaces
2. Navigate to the `backend-monitor` directory
3. The tool is ready to use (Python is pre-installed)

### System Requirements
- **OS**: Windows, macOS, or Linux
- **Python**: 3.10 or higher
- **Memory**: Minimal (processes files line-by-line)
- **Storage**: No additional storage required

## 📖 Usage Guide

### Basic Syntax
```bash
python monitor.py <path> <keyword> [options]
```

### Command-Line Arguments

#### Required Arguments
- `path`: Path to file or directory to scan
  - File: `path/to/file.log`
  - Directory: `path/to/logs/` (scans recursively)
- `keyword`: Search term or regex pattern

#### Optional Arguments
- `--file-type EXT`: Filter by file extension (e.g., `.log`, `.sql`)
- `--ignore-case`: Case-insensitive search (enabled by default)
- `--context-lines N`: Show N lines of context around matches
- `--regex`: Treat keyword as regex pattern
- `--export FILE`: Export results to file (txt or csv)

### Usage Examples

#### 1. Search for Errors in Log Files
```bash
# Search all .log files in a directory for "error"
python monitor.py /var/log/application/ error --file-type .log

# Search specific log file
python monitor.py /var/log/app.log error
```

#### 2. Monitor Database Operations
```bash
# Find all TRUNCATE operations in SQL dumps
python monitor.py /backup/database/ truncate --file-type .sql

# Search for INSERT statements
python monitor.py /data/dumps/ INSERT --file-type .sql
```

#### 3. Advanced Pattern Matching
```bash
# Use regex to find multiple error types
python monitor.py /logs/ "ERROR|WARN|CRITICAL" --regex

# Case-sensitive search (disable ignore-case)
python monitor.py /code/ "ClassName"  # Note: no --ignore-case flag
```

#### 4. Client Database Monitoring
```bash
# Monitor client database logs for security events
python monitor.py /client/db/logs/ "LOGIN|ACCESS_DENIED|UNAUTHORIZED"

# Track data modifications
python monitor.py /client/backups/ "UPDATE|DELETE|DROP" --file-type .sql

# Analyze error patterns
python monitor.py /client/error_logs/ "exception|traceback" --regex
```

#### 5. Search SQLite Databases
```bash
# Search for user data in SQLite database
python monitor.py /data/users.db "john@example.com" --file-type .db

# Find pending orders in database
python monitor.py /ecommerce/orders.db pending --file-type .sqlite

# Search across all database files in a directory
python monitor.py /databases/ "admin" --file-type .db
```

### Database File Usage

#### How Database Search Works
When you provide a path to a SQLite database file (`.db`, `.sqlite`, `.sqlite3`), the tool:

1. **Connects** to the SQLite database
2. **Queries all tables** in the database
3. **Searches every column** in every row of every table
4. **Applies regex/case-insensitive matching** to find your keyword
5. **Displays results** with table, column, and row information

#### Database Path Examples

**Single Database File:**
```bash
# Search in a specific database file
python monitor.py /path/to/users.db "john@example.com"

# Search for pending orders
python monitor.py ./inventory.db pending

# Case-sensitive search in database
python monitor.py /data/app.db "ADMIN"  # Note: no --ignore-case flag
```

**Directory with Database Files:**
```bash
# Search all .db files in a directory
python monitor.py /databases/ "error" --file-type .db

# Search SQLite files recursively
python monitor.py /project/data/ "test" --file-type .sqlite
```

#### Database Output Format
```
[database.db:table_name.column_name:row_number] content with **highlighted** keyword
```

Database Example:
```
[users.db:users.email:row1] john@**example**.com
[orders.db:orders.status:row3] **pending**
[inventory.db:products.name:row15] Wireless **Mouse**
```

### Output Format
```
[file.ext:line_number] content with **highlighted** keyword
[file.db:table.column:row] content with **highlighted** keyword
```

Examples:
```
[app.log:25] User authentication failed for **admin**
[db.sql:150] **TRUNCATE** TABLE user_sessions;
[users.db:users.name:row1] John **Doe**
[orders.db:orders.status:row2] **pending**
```

## 🗄️ Database Path Configuration

### Where to Add Database Paths

**Direct Database File Path:**
```bash
python monitor.py /full/path/to/database.db "search_keyword"
python monitor.py ./relative/path/database.sqlite "keyword"
python monitor.py database.db "keyword"  # In current directory
```

**Directory Containing Databases:**
```bash
python monitor.py /path/to/database/directory/ "keyword" --file-type .db
python monitor.py /client/databases/ "error" --file-type .sqlite
```

### Database Path Examples

#### Local Development
```bash
# SQLite database in project directory
python monitor.py ./data/users.db "admin@example.com"

# Database in parent directory
python monitor.py ../databases/app.db "pending"

# Multiple databases in data folder
python monitor.py ./data/ "john" --file-type .db
```

#### Production Server
```bash
# Database in application directory
python monitor.py /var/app/data/users.db "inactive"

# Database backups directory
python monitor.py /backup/databases/ "error" --file-type .sqlite

# Client database on network share
python monitor.py /mnt/client/db/inventory.db "out_of_stock"
```

#### Docker/Container Environments
```bash
# Database mounted as volume
python monitor.py /app/data/database.db "search_term"

# Database in container data directory
python monitor.py /data/db/ "admin" --file-type .db
```

### Database Path Best Practices

1. **Use Absolute Paths** for production scripts
2. **Use Relative Paths** for development/testing
3. **Include File Extension** when specifying single files
4. **Use --file-type Filter** when scanning directories
5. **Ensure Read Permissions** on database files
6. **Backup Databases** before running searches on production data

### Common Database Path Patterns

```bash
# Web application databases
/var/www/app/data/users.db
/opt/myapp/db/sessions.sqlite
/home/user/projects/ecommerce/orders.db

# Development databases
./data/test.db
../databases/dev.sqlite
/project/db/app.db

# Client system databases
/client/system/data/inventory.db
/customer/db/transactions.sqlite
/enterprise/data/employees.db
```

## 🎯 Client Database System Integration

### Typical Client Setup
1. **Identify Data Sources**:
   - Database log files (`postgresql.log`, `mysql.log`)
   - Application logs (`app.log`, `error.log`)
   - SQL dump files (`.sql`)
   - SQLite database files (`.db`, `.sqlite`)
   - Configuration files (`.conf`, `.ini`)

2. **Directory Structure**:
   ```
   /client/system/
   ├── logs/
   │   ├── app.log
   │   ├── db.log
   │   └── error.log
   ├── databases/
   │   ├── users.db
   │   ├── orders.sqlite
   │   └── analytics.db
   ├── backups/
   │   ├── daily_dump.sql
   │   └── weekly_backup.sql
   └── config/
       └── database.conf
   ```

3. **Monitoring Workflow**:
   - **Daily Checks**: Run automated scans for critical keywords
   - **Incident Response**: Quick search during outages
   - **Performance Analysis**: Track slow queries and errors
   - **Security Auditing**: Monitor access patterns and failed logins

### Common Monitoring Scenarios

#### Database Content Monitoring
```bash
# Search user data in database
python monitor.py /client/databases/users.db "admin@example.com"

# Find pending orders
python monitor.py /client/databases/orders.db pending

# Monitor inventory levels
python monitor.py /client/databases/inventory.db "out_of_stock"

# Search across all client databases
python monitor.py /client/databases/ "error" --file-type .db
```

#### Database Health Monitoring
```bash
# Check for connection issues
python monitor.py /client/logs/ "connection refused|timeout"

# Monitor transaction failures
python monitor.py /client/logs/ "transaction rolled back|deadlock"

# Track long-running queries
python monitor.py /client/logs/ "duration|slow query"
```

#### Security Event Tracking
```bash
# Failed authentication attempts
python monitor.py /client/logs/ "authentication failed|invalid credentials"

# Access control violations
python monitor.py /client/logs/ "permission denied|access denied"

# Suspicious activities
python monitor.py /client/logs/ "unusual|anomaly|suspicious"
```

#### Performance Monitoring
```bash
# Memory issues
python monitor.py /client/logs/ "out of memory|memory leak"

# Disk space warnings
python monitor.py /client/logs/ "disk full|no space"

# Network connectivity
python monitor.py /client/logs/ "network unreachable|connection lost"
```

#### Database Content Monitoring
```bash
# Search for sensitive data in databases
python monitor.py /client/databases/ "password|ssn|credit_card" --file-type .db

# Find inactive users
python monitor.py /client/databases/ "inactive|suspended" --file-type .sqlite

# Monitor order statuses
python monitor.py /client/databases/ "pending|cancelled|refunded" --file-type .db

# Check for admin users
python monitor.py /client/databases/ "admin|superuser" --file-type .sqlite
```

### Automation Integration

#### Cron Job Setup (Linux/Mac)
```bash
# Daily error summary
0 9 * * * cd /path/to/monitoring/backend-monitor && python monitor.py /client/logs/ error --export daily_errors.txt

# Hourly performance check
0 * * * * cd /path/to/monitoring/backend-monitor && python monitor.py /client/logs/ "slow|timeout" --export hourly_perf.txt
```

#### Windows Task Scheduler
```batch
# Create a batch file (monitor_errors.bat)
cd C:\path\to\monitoring\backend-monitor
python monitor.py C:\client\logs error --export errors.txt
```

#### Integration with Monitoring Systems
- **Nagios/Icinga**: Use as external check command
- **ELK Stack**: Pre-process logs before ingestion
- **Splunk**: Custom search command integration
- **Custom Scripts**: Incorporate into existing monitoring workflows

## 🔍 Advanced Features

### Regex Patterns for Complex Searches
```bash
# Email addresses
python monitor.py /logs/ "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b" --regex

# IP addresses
python monitor.py /logs/ "\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b" --regex

# Timestamps
python monitor.py /logs/ "\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}" --regex
```

### Context Lines
```bash
# Show 2 lines before and after matches
python monitor.py /logs/ error --context-lines 2
```

### Export Functionality
```bash
# Export to text file
python monitor.py /logs/ error --export results.txt

# Export to CSV (future feature)
python monitor.py /logs/ error --export results.csv
```

## 🐛 Troubleshooting

### Common Issues

#### "Path does not exist" Error
- Verify the file/directory path is correct
- Use absolute paths if relative paths fail
- Check file permissions

#### No Matches Found
- Verify keyword spelling and case sensitivity
- Try case-insensitive search (default)
- Use regex mode for complex patterns
- Check if file type filter is too restrictive

#### Performance Issues
- For very large files, consider splitting them
- Use file type filters to limit scan scope
- Avoid overly broad regex patterns

#### Encoding Errors
- Tool handles UTF-8 with error tolerance
- For files with special encoding, convert to UTF-8 first

### Debug Mode
Add print statements to `monitor.py` for debugging:
```python
print(f"Scanning file: {file_path}")
print(f"Found {len(matches)} matches")
```

## 📊 Performance Benchmarks

- **Small Files** (< 1MB): Instantaneous
- **Medium Files** (1MB - 100MB): < 1 second
- **Large Files** (100MB+): 1-5 seconds depending on pattern complexity
- **Directory Scanning**: Scales linearly with file count

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test thoroughly
4. Submit a pull request

### Development Guidelines
- Maintain single-script architecture
- Add comprehensive error handling
- Include docstrings for new functions
- Test with various file types and edge cases

## 📄 License

MIT License - See LICENSE file for details

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review existing GitHub issues
3. Create a new issue with:
   - Python version
   - OS details
   - Command used
   - Expected vs actual output

---

**Happy Monitoring!** 🔍