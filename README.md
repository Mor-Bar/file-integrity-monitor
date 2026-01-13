# File Integrity Monitor

A professional-grade file integrity monitoring tool for detecting unauthorized file modifications using cryptographic hash comparison. Built with enterprise-level best practices for security monitoring, compliance verification, and change detection.

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/code%20style-PEP8-brightgreen.svg)](https://www.python.org/dev/peps/pep-0008/)

## Overview

File Integrity Monitor (FIM) is a robust tool designed for security professionals and system administrators to maintain and verify file system integrity. It creates cryptographic baselines of file systems and efficiently detects modifications, additions, and deletions through hash-based comparison.

### Key Capabilities

- **Cryptographic Hashing**: Support for multiple algorithms (SHA256, SHA512, MD5, SHA1, BLAKE2)
- **Recursive Directory Scanning**: Efficient traversal with configurable ignore patterns
- **Change Detection**: Comprehensive identification of modified, added, and deleted files
- **Baseline Management**: JSON-based baseline creation, storage, and comparison
- **Pattern Filtering**: `.fimignore` file support for excluding files and directories
- **Structured Logging**: Detailed audit logs with configurable verbosity levels
- **Dual Interface**: Both interactive CLI menu and command-line arguments
- **Progress Tracking**: Visual feedback for long-running operations
- **Configuration Management**: JSON-based centralized configuration

## Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager
- Git (for cloning repository)

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/file-integrity-monitor.git
cd file-integrity-monitor
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\Activate.ps1

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Verify installation:
```bash
python run.py --version
```

## Usage

### Interactive Mode

Launch the interactive menu interface:

```bash
python run.py
```

The interactive mode provides a numbered menu with the following options:
1. Calculate hash of single file
2. Create baseline for directory
3. Display baseline information
4. Check for changes
0. Exit

### Command-Line Interface

#### Create Baseline

Generate a baseline snapshot of a directory:

```bash
python run.py create <directory> [--output BASELINE_FILE]
```

**Example:**
```bash
python run.py create ./src --output production_baseline.json
```

#### Detect Changes

Compare current directory state against baseline:

```bash
python run.py check <directory> [--baseline BASELINE_FILE]
```

**Example:**
```bash
python run.py check ./src --baseline production_baseline.json
```

#### Calculate File Hash

Compute hash for a single file:

```bash
python run.py hash <file_path>
```

**Example:**
```bash
python run.py hash /etc/passwd
```

#### Display Baseline

View baseline metadata and file inventory:

```bash
python run.py display [--baseline BASELINE_FILE]
```

#### Help

Access detailed command documentation:

```bash
python run.py --help
python run.py create --help
python run.py check --help
```

## Project Structure

```
file-integrity-monitor/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── baseline.py              # Baseline creation and loading
│   ├── config_loader.py         # Configuration management
│   ├── constants.py             # Application constants
│   ├── detector.py              # Change detection engine
│   ├── display.py               # Output formatting and reporting
│   ├── file_monitor.py          # Main CLI controller
│   ├── hash_calculator.py       # Cryptographic hash computation
│   ├── ignore_handler.py        # Pattern matching for file exclusion
│   ├── logger.py                # Logging configuration
│   └── scanner.py               # Directory traversal and scanning
├── tests/                        # Unit tests (future implementation)
├── venv/                         # Virtual environment (not in git)
├── .fimignore                   # File/directory exclusion patterns
├── .gitignore                   # Git exclusion patterns
├── config.json                  # Application configuration
├── LICENSE                      # MIT License
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
└── run.py                       # Application entry point
```

## Configuration

### Configuration File

The tool uses `config.json` for centralized configuration management. Default configuration:

```json
{
  "default_algorithm": "sha256",
  "default_baseline_file": "baseline.json",
  "default_ignore_file": ".fimignore",
  "chunk_size": 65536,
  "logging": {
    "enabled": true,
    "log_file": "file_monitor.log",
    "log_level": "INFO",
    "console_output": true
  },
  "display": {
    "separator_length": 50,
    "hash_display_length": 16,
    "verbose": true
  },
  "ignore_patterns": {
    "use_default_patterns": true,
    "custom_patterns": []
  }
}
```

### Ignore Patterns

Create a `.fimignore` file in the project root to exclude files and directories. Syntax is identical to `.gitignore`:

```
# Python artifacts
__pycache__/
*.pyc
*.pyo
*.pyd

# Virtual environments
venv/
env/
.venv/

# IDE configurations
.vscode/
.idea/
*.swp

# Logs
*.log

# OS files
.DS_Store
Thumbs.db
```

## Output Examples

### Baseline Creation

```
==================================================
Creating Baseline
==================================================

Scanning directory: ./src
==================================================
Processing files: 100%|████████████████| 11/11 [00:00<00:00, 156.25file/s]

Total files scanned: 11

✓ Baseline saved to: baseline.json
✓ Files tracked: 11
```

### Change Detection Report

```
==================================================
Change Detection Report
==================================================

Summary:
   Modified: 2
   Added: 1
   Deleted: 0
   Unchanged: 8
   Total changes: 3

--------------------------------------------------
MODIFIED FILES:
--------------------------------------------------

File: config.py
   Path: src/config.py
   Old hash: 2fed4727f5679a7b...
   New hash: 24c49e8ba88a60a7...
   Size: 1024 → 1156 bytes
   Modified: 2026-01-13T18:15:18.123456

File: utils.py
   Path: src/utils.py
   Old hash: 89abc123def456...
   New hash: 456def789abc123...
   Size: 512 → 678 bytes
   Modified: 2026-01-13T18:16:22.654321

--------------------------------------------------
ADDED FILES:
--------------------------------------------------

File: validator.py
   Path: src/validator.py
   Hash: a7f5d6e89b4c3a21...
   Size: 234 bytes
   Created: 2026-01-13T18:17:30.987654

==================================================
3 change(s) detected!
==================================================
```

## Use Cases

### Security Monitoring

- Detect unauthorized modifications to system files
- Monitor critical configuration files for tampering
- Identify rootkit or malware installations
- Track changes in sensitive directories

### Compliance and Auditing

- Meet regulatory requirements for file integrity verification
- Generate audit trails for change management
- Document system state at specific points in time
- Verify compliance with security baselines

### DevOps and System Administration

- Validate deployment integrity
- Detect configuration drift
- Monitor application file changes
- Verify backup and restore operations

### Forensics and Incident Response

- Establish pre-incident baselines
- Identify compromised files during investigations
- Document evidence chains
- Compare system states across time periods

## Technical Details

### Hash Algorithms

The tool supports multiple cryptographic hash functions:

- **SHA256** (default): 256-bit SHA-2 algorithm, NIST recommended
- **SHA512**: 512-bit SHA-2 algorithm for enhanced security
- **SHA1**: Legacy support (not recommended for security)
- **MD5**: Legacy support (not recommended for security)
- **BLAKE2**: Modern high-speed cryptographic hash

### Performance Optimization

- **Chunked Reading**: Files processed in 64KB chunks for memory efficiency
- **Progress Tracking**: Real-time feedback for long operations
- **Ignore Patterns**: Early filtering to skip unnecessary processing
- **Efficient Traversal**: Directory structure traversed once per operation

### Logging System

Comprehensive logging with multiple severity levels:

- **DEBUG**: Detailed diagnostic information
- **INFO**: General operational messages
- **WARNING**: Non-critical issues and skipped files
- **ERROR**: Operation failures and exceptions

Logs written to both console and `file_monitor.log` file.

## Dependencies

All dependencies are specified in `requirements.txt`:

```
tqdm>=4.66.0
```

All other functionality relies on Python standard library modules:
- `hashlib` - Cryptographic hashing
- `json` - JSON parsing and generation
- `argparse` - Command-line argument parsing
- `logging` - Logging framework
- `pathlib` - Path manipulation
- `os` - Operating system interface
- `datetime` - Timestamp handling
- `fnmatch` - Filename pattern matching

## Development

### Code Quality Standards

- **PEP 8**: Python code style guide compliance
- **Type Hints**: Function signatures include type annotations
- **Docstrings**: All modules, classes, and functions documented
- **Error Handling**: Comprehensive exception handling
- **Logging**: Structured logging throughout application

### Architecture

The application follows a modular architecture with separation of concerns:

- **Core Logic**: Hash calculation, scanning, detection
- **Interface Layer**: CLI argument parsing, interactive menu
- **Configuration**: Centralized settings management
- **Presentation**: Output formatting and reporting
- **Utility**: Logging, pattern matching, file I/O

## Contributing

Contributions are welcome. Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-capability`)
3. Commit changes with clear messages
4. Write or update tests as appropriate
5. Update documentation for new features
6. Submit a pull request with detailed description

## Testing

Unit tests are planned for future implementation. Test coverage will include:

- Hash calculation accuracy
- Baseline creation and loading
- Change detection logic
- Ignore pattern matching
- Configuration management
- Error handling scenarios

## License

This project is licensed under the MIT License. See the [MIT](LICENSE) file for complete license text.

## Author

**Mor Bar**
- Role: Cybersecurity R&D Engineer
- Location: Israel
- GitHub: [@Mor-Bar](https://github.com/Mor-Bar)

## Acknowledgments

This project was developed as part of a professional portfolio demonstrating:
- Secure software development practices
- File system security monitoring
- Python application architecture
- Command-line tool design

Inspired by industry-standard file integrity monitoring solutions used in enterprise security operations.

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Review existing documentation
- Check configuration settings
- Examine log files for diagnostic information

## Roadmap

Planned enhancements for future releases:

- [ ] Unit test suite with pytest
- [ ] Database backend for baseline storage
- [ ] Real-time monitoring daemon mode
- [ ] Email/webhook notifications for changes
- [ ] Multiple baseline comparison
- [ ] Differential reporting between baselines
- [ ] Support for extended file attributes
- [ ] Integration with SIEM systems
- [ ] Web-based dashboard interface

---

**Version:** 0.4
**Last Updated:** January 2026
**Status:** Production Ready