"""
Change detection utilities for file integrity monitoring.
"""

from .baseline import load_baseline
from .scanner import scan_directory
from .ignore_handler import IgnoreHandler
from .constants import MSG_SEPARATOR
from .logger import logger


def compare_with_baseline(directory_path, baseline_file='baseline.json'):
    """
    Compare current directory state with baseline and detect changes.
    
    Args:
        directory_path (str): Directory to scan
        baseline_file (str): Baseline JSON file path
    
    Returns:
        dict: Dictionary with changes categorized by type
    """
    logger.info(f"Starting change detection for: {directory_path}")
    
    print("\n" + MSG_SEPARATOR)
    print("Detecting Changes")
    print(MSG_SEPARATOR)
    
    # Load baseline
    baseline = load_baseline(baseline_file)
    
    # Get baseline info
    baseline_files = baseline['files']
    algorithm = baseline['metadata']['algorithm']
    
    # Initialize ignore handler with baseline patterns
    ignore_handler = IgnoreHandler()
    if 'ignore_patterns' in baseline['metadata']:
        for pattern in baseline['metadata']['ignore_patterns']:
            ignore_handler.add_pattern(pattern)
    
    # Scan current state
    current_files = scan_directory(directory_path, algorithm, verbose=True, ignore_handler=ignore_handler)
    
    # Initialize changes dictionary
    changes = {
        'modified': [],
        'added': [],
        'deleted': [],
        'unchanged': []
    }
    
    # Check for modified and unchanged files
    for file_path, current_info in current_files.items():
        if file_path in baseline_files:
            baseline_info = baseline_files[file_path]
            
            if current_info['hash'] != baseline_info['hash']:
                # File was modified
                changes['modified'].append({
                    'path': file_path,
                    'old_hash': baseline_info['hash'],
                    'new_hash': current_info['hash'],
                    'old_size': baseline_info['size'],
                    'new_size': current_info['size'],
                    'old_modified': baseline_info['modified'],
                    'new_modified': current_info['modified']
                })
                logger.info(f"Modified: {file_path}")
            else:
                # File unchanged
                changes['unchanged'].append(file_path)
        else:
            # File is new (added)
            changes['added'].append({
                'path': file_path,
                'hash': current_info['hash'],
                'size': current_info['size'],
                'modified': current_info['modified']
            })
            logger.info(f"Added: {file_path}")
    
    # Check for deleted files
    for file_path in baseline_files:
        if file_path not in current_files:
            changes['deleted'].append({
                'path': file_path,
                'hash': baseline_files[file_path]['hash'],
                'size': baseline_files[file_path]['size']
            })
            logger.info(f"Deleted: {file_path}")
    
    total_changes = len(changes['modified']) + len(changes['added']) + len(changes['deleted'])
    logger.info(f"Change detection completed: {total_changes} changes found")
    
    return changes