"""
File Integrity Monitor - Basic Hash Calculator
A simple tool to calculate SHA256 hash of a file
"""

import hashlib
import os


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
    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Check if it's a file (not directory)
    if not os.path.isfile(file_path):
        raise ValueError(f"Path is not a file: {file_path}")
    
    # Create hash object
    hash_obj = hashlib.new(algorithm)
    
    # Read file in chunks to handle large files efficiently
    try:
        with open(file_path, 'rb') as f:
            # Read in 64kb chunks
            chunk_size = 65536
            while chunk := f.read(chunk_size):
                hash_obj.update(chunk)
    except PermissionError:
        raise PermissionError(f"Permission denied: {file_path}")
    
    return hash_obj.hexdigest()


def main():
    """Main function - basic usage example"""
    print("=" * 50)
    print("File Integrity Monitor - Hash Calculator")
    print("=" * 50)
    
    # Get file path from user
    file_path = input("\nEnter file path: ").strip()
    
    try:
        # Calculate hash
        file_hash = calculate_file_hash(file_path)
        
        # Display results
        print(f"\n✓ File: {file_path}")
        print(f"✓ SHA256: {file_hash}")
        
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
    except ValueError as e:
        print(f"\n✗ Error: {e}")
    except PermissionError as e:
        print(f"\n✗ Error: {e}")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")


if __name__ == "__main__":
    main()