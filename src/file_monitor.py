"""
File Integrity Monitor - Baseline Creation
A tool to create and manage file integrity baselines
"""

import hashlib
import os
import json
from datetime import datetime
from pathlib import Path


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
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not os.path.isfile(file_path):
        raise ValueError(f"Path is not a file: {file_path}")
    
    hash_obj = hashlib.new(algorithm)
    
    try:
        with open(file_path, 'rb') as f:
            chunk_size = 65536
            while chunk := f.read(chunk_size):
                hash_obj.update(chunk)
    except PermissionError:
        raise PermissionError(f"Permission denied: {file_path}")
    
    return hash_obj.hexdigest()


def scan_directory(directory_path, algorithm='sha256'):
    """
    Scan a directory and calculate hashes for all files.
    
    Args:
        directory_path (str): Path to directory to scan
        algorithm (str): Hash algorithm to use
    
    Returns:
        dict: Dictionary with file paths as keys and hash info as values
    """
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"Directory not found: {directory_path}")
    
    if not os.path.isdir(directory_path):
        raise ValueError(f"Path is not a directory: {directory_path}")
    
    results = {}
    file_count = 0
    
    print(f"\n🔍 Scanning directory: {directory_path}")
    print("=" * 50)
    
    # Walk through directory
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            
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
                print(f"✓ [{file_count}] {filename}")
                
            except (PermissionError, OSError) as e:
                print(f"✗ Skipped {filename}: {e}")
                continue
    
    print(f"\n📊 Total files scanned: {file_count}")
    return results


def create_baseline(directory_path, baseline_file='baseline.json', algorithm='sha256'):
    """
    Create a baseline snapshot of a directory.
    
    Args:
        directory_path (str): Directory to scan
        baseline_file (str): Output JSON file path
        algorithm (str): Hash algorithm to use
    
    Returns:
        dict: Baseline data
    """
    print("\n" + "=" * 50)
    print("Creating Baseline")
    print("=" * 50)
    
    # Scan directory
    scan_results = scan_directory(directory_path, algorithm)
    
    # Create baseline structure
    baseline = {
        'metadata': {
            'created': datetime.now().isoformat(),
            'directory': os.path.abspath(directory_path),
            'algorithm': algorithm,
            'file_count': len(scan_results)
        },
        'files': scan_results
    }
    
    # Save to JSON file
    with open(baseline_file, 'w', encoding='utf-8') as f:
        json.dump(baseline, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Baseline saved to: {baseline_file}")
    print(f"✓ Files tracked: {len(scan_results)}")
    
    return baseline


def display_baseline(baseline_file='baseline.json'):
    """
    Display the contents of a baseline file.
    
    Args:
        baseline_file (str): Path to baseline JSON file
    """
    if not os.path.exists(baseline_file):
        print(f"✗ Baseline file not found: {baseline_file}")
        return
    
    with open(baseline_file, 'r', encoding='utf-8') as f:
        baseline = json.load(f)
    
    print("\n" + "=" * 50)
    print("Baseline Information")
    print("=" * 50)
    
    metadata = baseline['metadata']
    print(f"\n📅 Created: {metadata['created']}")
    print(f"📁 Directory: {metadata['directory']}")
    print(f"🔐 Algorithm: {metadata['algorithm']}")
    print(f"📊 Files tracked: {metadata['file_count']}")
    
    print("\n" + "-" * 50)
    print("Files:")
    print("-" * 50)
    
    for file_path, info in baseline['files'].items():
        filename = os.path.basename(file_path)
        print(f"\n📄 {filename}")
        print(f"   Hash: {info['hash'][:16]}...")
        print(f"   Size: {info['size']} bytes")
        print(f"   Modified: {info['modified']}")


def main():
    """Main function with menu"""
    print("=" * 50)
    print("File Integrity Monitor v0.2")
    print("=" * 50)
    
    print("\nOptions:")
    print("1. Calculate hash of single file")
    print("2. Create baseline for directory")
    print("3. Display baseline")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        # Single file hash
        file_path = input("Enter file path: ").strip()
        try:
            file_hash = calculate_file_hash(file_path)
            print(f"\n✓ File: {file_path}")
            print(f"✓ SHA256: {file_hash}")
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    elif choice == '2':
        # Create baseline
        directory = input("Enter directory path to scan: ").strip()
        baseline_file = input("Baseline filename (default: baseline.json): ").strip()
        if not baseline_file:
            baseline_file = 'baseline.json'
        
        try:
            create_baseline(directory, baseline_file)
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    elif choice == '3':
        # Display baseline
        baseline_file = input("Baseline filename (default: baseline.json): ").strip()
        if not baseline_file:
            baseline_file = 'baseline.json'
        
        display_baseline(baseline_file)
    
    else:
        print("\n✗ Invalid choice!")


if __name__ == "__main__":
    main()