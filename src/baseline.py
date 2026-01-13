"""
Baseline management utilities for file integrity monitoring.
"""

import json
import os
from datetime import datetime
from .scanner import scan_directory
from .ignore_handler import IgnoreHandler
from .constants import DEFAULT_ALGORITHM, MSG_SEPARATOR
from .logger import logger


def create_baseline(directory_path, baseline_file='baseline.json', algorithm=DEFAULT_ALGORITHM):
    """
    Create a baseline snapshot of a directory.
    
    Args:
        directory_path (str): Directory to scan
        baseline_file (str): Output JSON file path
        algorithm (str): Hash algorithm to use
    
    Returns:
        dict: Baseline data
    """
    logger.info(f"Creating baseline for: {directory_path}")
    
    print("\n" + MSG_SEPARATOR)
    print("Creating Baseline")
    print(MSG_SEPARATOR)
    
    # Initialize ignore handler
    ignore_handler = IgnoreHandler()
    
    # Scan directory
    scan_results = scan_directory(directory_path, algorithm, verbose=True, ignore_handler=ignore_handler)
    
    # Create baseline structure
    baseline = {
        'metadata': {
            'created': datetime.now().isoformat(),
            'directory': os.path.abspath(directory_path),
            'algorithm': algorithm,
            'file_count': len(scan_results),
            'ignore_patterns': ignore_handler.get_patterns()
        },
        'files': scan_results
    }
    
    # Save to JSON file
    try:
        with open(baseline_file, 'w', encoding='utf-8') as f:
            json.dump(baseline, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Baseline saved to: {baseline_file}")
        print(f"✓ Files tracked: {len(scan_results)}")
        
        logger.info(f"Baseline created successfully: {baseline_file}")
        
    except Exception as e:
        logger.error(f"Failed to save baseline: {e}")
        raise
    
    return baseline


def load_baseline(baseline_file='baseline.json'):
    """
    Load a baseline from a JSON file.
    
    Args:
        baseline_file (str): Path to baseline JSON file
    
    Returns:
        dict: Baseline data
    
    Raises:
        FileNotFoundError: If baseline file doesn't exist
    """
    logger.debug(f"Loading baseline from: {baseline_file}")
    
    if not os.path.exists(baseline_file):
        logger.error(f"Baseline file not found: {baseline_file}")
        raise FileNotFoundError(f"Baseline file not found: {baseline_file}")
    
    try:
        with open(baseline_file, 'r', encoding='utf-8') as f:
            baseline = json.load(f)
        
        logger.info(f"Baseline loaded: {baseline['metadata']['file_count']} files")
        return baseline
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid baseline file format: {e}")
        raise ValueError(f"Invalid baseline file format: {e}") from e