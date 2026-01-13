"""
File Integrity Monitor - Main CLI
A tool to create baselines and detect file changes
"""

from .hash_calculator import calculate_file_hash
from .baseline import create_baseline
from .detector import compare_with_baseline
from .display import display_baseline, display_changes


def print_menu():
    """Print the main menu."""
    print("\n" + "=" * 50)
    print("File Integrity Monitor v0.3")
    print("=" * 50)
    print("\nOptions:")
    print("1. Calculate hash of single file")
    print("2. Create baseline for directory")
    print("3. Display baseline")
    print("4. Check for changes")
    print("0. Exit")


def handle_single_file_hash():
    """Handle single file hash calculation."""
    file_path = input("\nEnter file path: ").strip()
    try:
        file_hash = calculate_file_hash(file_path)
        print(f"\n✓ File: {file_path}")
        print(f"✓ SHA256: {file_hash}")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def handle_create_baseline():
    """Handle baseline creation."""
    directory = input("\nEnter directory path to scan: ").strip()
    baseline_file = input("Baseline filename (default: baseline.json): ").strip()
    if not baseline_file:
        baseline_file = 'baseline.json'
    
    try:
        create_baseline(directory, baseline_file)
    except Exception as e:
        print(f"\n✗ Error: {e}")


def handle_display_baseline():
    """Handle baseline display."""
    baseline_file = input("\nBaseline filename (default: baseline.json): ").strip()
    if not baseline_file:
        baseline_file = 'baseline.json'
    
    display_baseline(baseline_file)


def handle_check_changes():
    """Handle change detection."""
    directory = input("\nEnter directory path to check: ").strip()
    baseline_file = input("Baseline filename (default: baseline.json): ").strip()
    if not baseline_file:
        baseline_file = 'baseline.json'
    
    try:
        changes = compare_with_baseline(directory, baseline_file)
        display_changes(changes)
    except Exception as e:
        print(f"\n✗ Error: {e}")


def main():
    """Main function with menu loop."""
    while True:
        print_menu()
        choice = input("\nEnter choice (0-4): ").strip()
        
        if choice == '0':
            print("\n👋 Goodbye!")
            break
        elif choice == '1':
            handle_single_file_hash()
        elif choice == '2':
            handle_create_baseline()
        elif choice == '3':
            handle_display_baseline()
        elif choice == '4':
            handle_check_changes()
        else:
            print("\n✗ Invalid choice! Please enter 0-4.")
        
        # Pause before showing menu again
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()