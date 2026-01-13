"""
Hash calculation utilities for file integrity monitoring.
"""

import hashlib
import os
from .constants import CHUNK_SIZE
from .logger import logger


def calculate_file_hash(file_path, algorithm='sha256'):
    """
    Calculate hash of a file using specified algorithm.
    
    Args:
        file_path (str): Path to the file
        algorithm (str): Hash algorithm to use (default: sha256)
    
    Returns:
        str: Hexadecimal hash string
    
    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If file cannot be read
    """
    logger.debug(f"Calculating {algorithm} hash for: {file_path}")
    
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not os.path.isfile(file_path):
        logger.error(f"Path is not a file: {file_path}")
        raise ValueError(f"Path is not a file: {file_path}")
    
    try:
        hash_obj = hashlib.new(algorithm)
    except ValueError as e:
        logger.error(f"Unsupported hash algorithm: {algorithm}")
        raise ValueError(f"Unsupported hash algorithm: {algorithm}") from e
    
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(CHUNK_SIZE):
                hash_obj.update(chunk)
        
        result = hash_obj.hexdigest()
        logger.debug(f"Hash calculated successfully: {result[:16]}...")
        return result
        
    except PermissionError as e:
        logger.error(f"Permission denied: {file_path}")
        raise PermissionError(f"Permission denied: {file_path}") from e