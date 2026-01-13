"""
File Integrity Monitor - Main CLI
A tool to create baselines and detect file changes
"""

import argparse
import sys
from .hash_calculator import calculate_file_hash
from .baseline import create_baseline
from .detector import compare_with_baseline
from .display import display_baseline, display_changes
from .config_loader import get_config
from .logger import logger


def print_menu():
    """Print the main menu."""
    print("\n" + "=" * 50)
    print("File Integrity Monitor v0.4")
    print("=" * 50)
    print("\nOptions:")
    print("1. Calculate hash of single file")
    print("2. Create baseline for directory")
    print("3. Display baseline")
    print("4. Check for changes")
    print("0. Exit")


def handle_single_file_hash(file_path=None):
    """Handle single file hash calculation."""
    if file_path is None:
        file_path = input("\nEnter file path: ").strip()
    
    try:
        config = get_config()
        algorithm = str(config.get('default_algorithm', 'sha256'))
        file_hash = calculate_file_hash(file_path, algorithm)
        print(f"\n✓ File: {file_path}")
        print(f"✓ {algorithm.upper()}: {file_hash}")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        logger.error(f"Failed to calculate hash: {e}")


def handle_create_baseline(directory=None, baseline_file=None):
    """Handle baseline creation."""
    config = get_config()
    
    if directory is None:
        directory = input("\nEnter directory path to scan: ").strip()
    
    if baseline_file is None:
        default_baseline = str(config.get('default_baseline_file', 'baseline.json'))
        baseline_input = input(f"Baseline filename (default: {default_baseline}): ").strip()
        baseline_file = baseline_input if baseline_input else default_baseline
    
    try:
        algorithm = str(config.get('default_algorithm', 'sha256'))
        create_baseline(directory, baseline_file, algorithm)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        logger.error(f"Failed to create baseline: {e}")


def handle_display_baseline(baseline_file=None):
    """Handle baseline display."""
    config = get_config()
    
    if baseline_file is None:
        default_baseline = str(config.get('default_baseline_file', 'baseline.json'))
        baseline_input = input(f"\nBaseline filename (default: {default_baseline}): ").strip()
        baseline_file = baseline_input if baseline_input else default_baseline
    
    display_baseline(baseline_file)


def handle_check_changes(directory=None, baseline_file=None):
    """Handle change detection."""
    config = get_config()
    
    if directory is None:
        directory = input("\nEnter directory path to check: ").strip()
    
    if baseline_file is None:
        default_baseline = str(config.get('default_baseline_file', 'baseline.json'))
        baseline_input = input(f"Baseline filename (default: {default_baseline}): ").strip()
        baseline_file = baseline_input if baseline_input else default_baseline
    
    try:
        changes = compare_with_baseline(directory, baseline_file)
        display_changes(changes)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        logger.error(f"Failed to check changes: {e}")


def interactive_mode():
    """Run in interactive menu mode."""
    logger.info("Starting interactive mode")
    
    while True:
        print_menu()
        choice = input("\nEnter choice (0-4): ").strip()
        
        if choice == '0':
            print("\n👋 Goodbye!")
            logger.info("Exiting application")
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


def cli_mode():
    """Run in CLI mode with arguments."""
    parser = argparse.ArgumentParser(
        description='File Integrity Monitor - Detect file changes using hash comparison',
        epilog='Example: python run.py create src --output baseline.json'
    )
    
    # Add version
    parser.add_argument('--version', action='version', version='File Integrity Monitor 0.4')
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Hash command
    hash_parser = subparsers.add_parser('hash', help='Calculate hash of a single file')
    hash_parser.add_argument('file', help='File path')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a baseline')
    create_parser.add_argument('directory', help='Directory to scan')
    create_parser.add_argument('-o', '--output', default=None, help='Output baseline file (default: baseline.json)')
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Check for changes')
    check_parser.add_argument('directory', help='Directory to check')
    check_parser.add_argument('-b', '--baseline', default=None, help='Baseline file (default: baseline.json)')
    
    # Display command
    display_parser = subparsers.add_parser('display', help='Display baseline information')
    display_parser.add_argument('-b', '--baseline', default=None, help='Baseline file (default: baseline.json)')
    
    # Interactive command (default)
    subparsers.add_parser('interactive', help='Run in interactive menu mode')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Get config for defaults
    config = get_config()
    
    # Execute command
    if args.command == 'hash':
        handle_single_file_hash(args.file)
    
    elif args.command == 'create':
        output_file = args.output if args.output else str(config.get('default_baseline_file', 'baseline.json'))
        handle_create_baseline(args.directory, output_file)
    
    elif args.command == 'check':
        baseline_file = args.baseline if args.baseline else str(config.get('default_baseline_file', 'baseline.json'))
        handle_check_changes(args.directory, baseline_file)
    
    elif args.command == 'display':
        baseline_file = args.baseline if args.baseline else str(config.get('default_baseline_file', 'baseline.json'))
        handle_display_baseline(baseline_file)
    
    elif args.command == 'interactive':
        interactive_mode()
    
    else:
        # No command provided - show help or run interactive
        if len(sys.argv) == 1:
            # No arguments at all - run interactive mode
            interactive_mode()
        else:
            parser.print_help()

def main():
    """Main entry point."""
    logger.info("File Integrity Monitor started")
    
    try:
        cli_mode()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        logger.info("Application interrupted by user")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()