"""
Logging configuration for File Integrity Monitor.
"""

import logging
import sys
from .constants import LOG_FILE, LOG_FORMAT, LOG_DATE_FORMAT


def setup_logger(name='FileIntegrityMonitor', level=logging.INFO, log_to_file=True):
    """
    Set up a logger with both console and file handlers.
    
    Args:
        name (str): Logger name
        level (int): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file (bool): Whether to log to file
    
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    
    # Console handler (INFO and above)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (DEBUG and above) - if enabled
    if log_to_file:
        try:
            file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Could not create log file: {e}")
    
    return logger


# Create default logger instance
logger = setup_logger()