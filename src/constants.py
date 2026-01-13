"""
Constants and configuration values for File Integrity Monitor.
"""

# Hash algorithm settings
DEFAULT_ALGORITHM = 'sha256'
SUPPORTED_ALGORITHMS = ['md5', 'sha1', 'sha256', 'sha512', 'blake2b']

# File I/O settings
CHUNK_SIZE = 65536  # 64KB chunks for file reading

# Baseline settings
DEFAULT_BASELINE_FILE = 'baseline.json'

# Display settings
SEPARATOR_LENGTH = 50
HASH_DISPLAY_LENGTH = 16  # Show first 16 chars of hash

# Ignore patterns
DEFAULT_IGNORE_FILE = '.fimignore'
DEFAULT_IGNORE_PATTERNS = [
    '__pycache__',
    '*.pyc',
    '*.pyo',
    '.git',
    '.gitignore',
    '.DS_Store',
    'Thumbs.db',
    '*.log',
    '.vscode',
    '.idea',
    'node_modules',
    'venv',
    'env',
    '.env',
]

# Logging settings
LOG_FILE = 'file_monitor.log'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# CLI Messages
MSG_SEPARATOR = "=" * SEPARATOR_LENGTH
MSG_SUB_SEPARATOR = "-" * SEPARATOR_LENGTH