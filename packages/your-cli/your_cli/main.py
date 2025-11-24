"""
Main entry point for the CLI.
"""

import argparse
import sys
from typing import List, Optional


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the CLI.
    
    Args:
        args: Command line arguments (defaults to sys.argv[1:])
        
    Returns:
        Exit code
    """
    if args is None:
        args = sys.argv[1:]
        
    parser = argparse.ArgumentParser(description="Your CLI tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Add commands here
    setup_parser = subparsers.add_parser("setup", help="Setup the project")
    setup_parser.add_argument("--force", action="store_true", help="Force setup")
    
    run_parser = subparsers.add_parser("run", help="Run a task")
    run_parser.add_argument("task", help="Task to run")
    
    parsed_args = parser.parse_args(args)
    
    if parsed_args.command == "setup":
        return setup_command(parsed_args)
    elif parsed_args.command == "run":
        return run_command(parsed_args)
    else:
        parser.print_help()
        return 1


def setup_command(args: argparse.Namespace) -> int:
    """
    Setup command implementation.
    
    Args:
        args: Parsed arguments
        
    Returns:
        Exit code
    """
    print(f"Setting up project (force={args.force})")
    return 0


def run_command(args: argparse.Namespace) -> int:
    """
    Run command implementation.
    
    Args:
        args: Parsed arguments
        
    Returns:
        Exit code
    """
    print(f"Running task: {args.task}")
    return 0


if __name__ == "__main__":
    sys.exit(main()) 