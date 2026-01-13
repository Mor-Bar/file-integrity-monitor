"""
Display and reporting utilities for file integrity monitoring.
"""

import os
from .baseline import load_baseline
from .constants import MSG_SEPARATOR, MSG_SUB_SEPARATOR, HASH_DISPLAY_LENGTH
from .logger import logger


def display_changes(changes):
    """
    Display detected changes in a formatted way.
    
    Args:
        changes (dict): Dictionary with categorized changes
    """
    logger.debug("Displaying change report")
    
    print("\n" + MSG_SEPARATOR)
    print("📋 Change Detection Report")
    print(MSG_SEPARATOR)
    
    # Statistics
    total_changes = len(changes['modified']) + len(changes['added']) + len(changes['deleted'])
    
    print(f"\n📊 Summary:")
    print(f"   🔴 Modified: {len(changes['modified'])}")
    print(f"   🟢 Added: {len(changes['added'])}")
    print(f"   🟡 Deleted: {len(changes['deleted'])}")
    print(f"   ⚪ Unchanged: {len(changes['unchanged'])}")
    print(f"   📈 Total changes: {total_changes}")
    
    # Modified files
    if changes['modified']:
        print("\n" + MSG_SUB_SEPARATOR)
        print("🔴 MODIFIED FILES:")
        print(MSG_SUB_SEPARATOR)
        for item in changes['modified']:
            filename = os.path.basename(item['path'])
            print(f"\n📄 {filename}")
            print(f"   Path: {item['path']}")
            print(f"   Old hash: {item['old_hash'][:HASH_DISPLAY_LENGTH]}...")
            print(f"   New hash: {item['new_hash'][:HASH_DISPLAY_LENGTH]}...")
            print(f"   Size: {item['old_size']} → {item['new_size']} bytes")
            print(f"   Modified: {item['new_modified']}")
    
    # Added files
    if changes['added']:
        print("\n" + MSG_SUB_SEPARATOR)
        print("🟢 ADDED FILES:")
        print(MSG_SUB_SEPARATOR)
        for item in changes['added']:
            filename = os.path.basename(item['path'])
            print(f"\n📄 {filename}")
            print(f"   Path: {item['path']}")
            print(f"   Hash: {item['hash'][:HASH_DISPLAY_LENGTH]}...")
            print(f"   Size: {item['size']} bytes")
            print(f"   Created: {item['modified']}")
    
    # Deleted files
    if changes['deleted']:
        print("\n" + MSG_SUB_SEPARATOR)
        print("🟡 DELETED FILES:")
        print(MSG_SUB_SEPARATOR)
        for item in changes['deleted']:
            filename = os.path.basename(item['path'])
            print(f"\n📄 {filename}")
            print(f"   Path: {item['path']}")
            print(f"   Last hash: {item['hash'][:HASH_DISPLAY_LENGTH]}...")
            print(f"   Last size: {item['size']} bytes")
    
    # Overall status
    print("\n" + MSG_SEPARATOR)
    if total_changes == 0:
        print("✅ No changes detected - all files match baseline!")
        logger.info("No changes detected")
    else:
        print(f"⚠️  {total_changes} change(s) detected!")
        logger.warning(f"{total_changes} changes detected")
    print(MSG_SEPARATOR)


def display_baseline(baseline_file='baseline.json'):
    """
    Display the contents of a baseline file.
    
    Args:
        baseline_file (str): Path to baseline JSON file
    """
    logger.debug(f"Displaying baseline: {baseline_file}")
    
    try:
        baseline = load_baseline(baseline_file)
    except FileNotFoundError:
        print(f"\n✗ Baseline file not found: {baseline_file}")
        logger.error(f"Baseline file not found: {baseline_file}")
        return
    
    print("\n" + MSG_SEPARATOR)
    print("Baseline Information")
    print(MSG_SEPARATOR)
    
    metadata = baseline['metadata']
    print(f"\n📅 Created: {metadata['created']}")
    print(f"📁 Directory: {metadata['directory']}")
    print(f"🔐 Algorithm: {metadata['algorithm']}")
    print(f"📊 Files tracked: {metadata['file_count']}")
    
    if 'ignore_patterns' in metadata and metadata['ignore_patterns']:
        print(f"🚫 Ignore patterns: {len(metadata['ignore_patterns'])} patterns")
    
    print("\n" + MSG_SUB_SEPARATOR)
    print("Files:")
    print(MSG_SUB_SEPARATOR)
    
    for file_path, info in baseline['files'].items():
        filename = os.path.basename(file_path)
        print(f"\n📄 {filename}")
        print(f"   Hash: {info['hash'][:HASH_DISPLAY_LENGTH]}...")
        print(f"   Size: {info['size']} bytes")
        print(f"   Modified: {info['modified']}")