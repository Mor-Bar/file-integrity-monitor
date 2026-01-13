"""
Directory scanning utilities for file integrity monitoring.
"""

import os
from datetime import datetime
from tqdm import tqdm
from .hash_calculator import calculate_file_hash
from .ignore_handler import IgnoreHandler
from .logger import logger


def scan_directory(directory_path, algorithm='sha256', verbose=True, ignore_handler=None):
    """
    Scan a directory and calculate hashes for all files.
    
    Args:
        directory_path (str): Path to directory to scan
        algorithm (str): Hash algorithm to use
        verbose (bool): Print progress messages
        ignore_handler (IgnoreHandler): Handler for ignore patterns
    
    Returns:
        dict: Dictionary with file paths as keys and hash info as values
    """
    logger.info(f"Starting directory scan: {directory_path}")
    
    if not os.path.exists(directory_path):
        logger.error(f"Directory not found: {directory_path}")
        raise FileNotFoundError(f"Directory not found: {directory_path}")
    
    if not os.path.isdir(directory_path):
        logger.error(f"Path is not a directory: {directory_path}")
        raise ValueError(f"Path is not a directory: {directory_path}")
    
    # Initialize ignore handler if not provided
    if ignore_handler is None:
        ignore_handler = IgnoreHandler()
    
    results = {}
    file_count = 0
    skipped_count = 0
    
    if verbose:
        print(f"\n🔍 Scanning directory: {directory_path}")
        print("=" * 50)
    
    # First pass: count total files and build file list
    file_list = []
    for root, dirs, files in os.walk(directory_path):
        # Filter out ignored directories (modify in-place to prevent walking into them)
        dirs[:] = [d for d in dirs if not ignore_handler.should_ignore(os.path.join(root, d))]
        
        for filename in files:
            file_path = os.path.join(root, filename)
            if not ignore_handler.should_ignore(file_path):
                file_list.append(file_path)
    
    # Second pass: process files with progress bar
    if verbose and len(file_list) > 0:
        pbar = tqdm(file_list, desc="Processing files", unit="file", 
                   ncols=100, bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]')
    else:
        pbar = file_list
    
    for file_path in pbar:
        try:
            # Calculate hash
            file_hash = calculate_file_hash(file_path, algorithm)
            
            # Get file info
            file_stat = os.stat(file_path)
            
            # Store results
            results[file_path] = {
                'hash': file_hash,
                'size': file_stat.st_size,
                'modified': datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                'algorithm': algorithm
            }
            
            file_count += 1
            logger.debug(f"Scanned file: {file_path}")
            
        except (PermissionError, OSError) as e:
            logger.warning(f"Could not scan {file_path}: {e}")
            skipped_count += 1
            continue
    
    if verbose:
        print(f"\n📊 Total files scanned: {file_count}")
        if skipped_count > 0:
            print(f"⚠️  Files skipped/ignored: {skipped_count}")
    
    logger.info(f"Scan completed: {file_count} files processed, {skipped_count} skipped")
    return results