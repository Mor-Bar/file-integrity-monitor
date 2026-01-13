"""
Ignore patterns handler for File Integrity Monitor.
"""

import os
import fnmatch
from .constants import DEFAULT_IGNORE_FILE, DEFAULT_IGNORE_PATTERNS
from .logger import logger


class IgnoreHandler:
    """Handle file and directory ignore patterns."""
    
    def __init__(self, ignore_file=None):
        """
        Initialize ignore handler.
        
        Args:
            ignore_file (str): Path to ignore file (like .fimignore)
        """
        self.patterns = list(DEFAULT_IGNORE_PATTERNS)
        
        if ignore_file and os.path.exists(ignore_file):
            self._load_ignore_file(ignore_file)
        elif os.path.exists(DEFAULT_IGNORE_FILE):
            self._load_ignore_file(DEFAULT_IGNORE_FILE)
    
    def _load_ignore_file(self, ignore_file):
        """
        Load patterns from ignore file.
        
        Args:
            ignore_file (str): Path to ignore file
        """
        try:
            with open(ignore_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if line and not line.startswith('#'):
                        self.patterns.append(line)
            logger.info(f"Loaded ignore patterns from: {ignore_file}")
        except Exception as e:
            logger.warning(f"Could not load ignore file {ignore_file}: {e}")
    
    def should_ignore(self, path):
        """
        Check if a path should be ignored.
        
        Args:
            path (str): File or directory path to check
        
        Returns:
            bool: True if path should be ignored
        """
        # Get basename and full path for matching
        basename = os.path.basename(path)
        
        for pattern in self.patterns:
            # Check basename match
            if fnmatch.fnmatch(basename, pattern):
                return True
            
            # Check full path match (for directory patterns)
            if fnmatch.fnmatch(path, f"*{pattern}*"):
                return True
            
            # Check if any parent directory matches
            path_parts = path.split(os.sep)
            for part in path_parts:
                if fnmatch.fnmatch(part, pattern):
                    return True
        
        return False
    
    def add_pattern(self, pattern):
        """
        Add a new ignore pattern.
        
        Args:
            pattern (str): Pattern to add
        """
        if pattern not in self.patterns:
            self.patterns.append(pattern)
            logger.debug(f"Added ignore pattern: {pattern}")
    
    def get_patterns(self):
        """
        Get all current ignore patterns.
        
        Returns:
            list: List of ignore patterns
        """
        return self.patterns.copy()