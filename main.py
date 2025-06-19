"""
Simple File Mover CLI
A clean, functional approach to moving files and folders.
"""

import os
import shutil
import sys
from pathlib import Path
from tkinter import filedialog
import tkinter as tk


def show_banner():
    """Display program banner"""
    print("=" * 60)
    print("         PYTHON FILE MOVER CLI")
    print("         Version 1.0.0")
    print("=" * 60)
    print()


def get_directory(prompt_text):
    """Get directory path using file dialog"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    print(f"{prompt_text}")
    print("Opening file dialog...")
    
    directory = filedialog.askdirectory(title=prompt_text)
    root.destroy()
    
    if not directory:
        print("No directory selected. Exiting...")
        sys.exit(1)
    
    print(f"Selected: {directory}")
    return directory


def get_extensions():
    """Get file extensions from user input"""
    extensions = []
    print("\nEnter file extensions to move (without dots, e.g., 'txt', 'pdf'):")
    print("Type 'done' when finished.")
    
    while True:
        ext = input("Extension: ").strip().lower()
        if ext == 'done':
            break
        if ext and ext not in extensions:
            extensions.append(ext)
            print(f"Added: .{ext}")
        elif ext in extensions:
            print(f".{ext} already added")
    
    return extensions


def confirm_action(message):
    """Get user confirmation"""
    while True:
        response = input(f"{message} (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        print("Please enter 'y' or 'n'")


def move_files_by_extension(source_dir, dest_dir, extensions):
    """Move files with specified extensions from source to destination"""
    source_path = Path(source_dir)
    dest_path = Path(dest_dir)
    
    if not source_path.exists():
        print(f"Error: Source directory '{source_dir}' does not exist")
        return False
    
    if not dest_path.exists():
        print(f"Error: Destination directory '{dest_dir}' does not exist")
        return False
    
    moved_count = 0
    
    print(f"\nSearching for files with extensions: {', '.join(f'.{ext}' for ext in extensions)}")
    
    for file_path in source_path.iterdir():
        if file_path.is_file():
            file_ext = file_path.suffix.lstrip('.').lower()
            if file_ext in extensions:
                try:
                    dest_file = dest_path / file_path.name
                    shutil.move(str(file_path), str(dest_file))
                    print(f"Moved: {file_path.name}")
                    moved_count += 1
                except Exception as e:
                    print(f"Error moving {file_path.name}: {e}")
    
    print(f"\nCompleted! Moved {moved_count} files.")
    return True


def move_folder(source_dir, dest_dir):
    """Move entire folder from source to destination"""
    source_path = Path(source_dir)
    dest_path = Path(dest_dir)
    
    if not source_path.exists():
        print(f"Error: Source directory '{source_dir}' does not exist")
        return False
    
    if not dest_path.exists():
        print(f"Error: Destination directory '{dest_dir}' does not exist")
        return False
    
    folder_name = source_path.name
    final_dest = dest_path / folder_name
    
    try:
        shutil.move(str(source_path), str(final_dest))
        print(f"Successfully moved folder '{folder_name}' to '{dest_dir}'")
        return True
    except Exception as e:
        print(f"Error moving folder: {e}")
        return False


def delete_permanently(path):
    """Permanently delete file or folder"""
    if not os.path.exists(path):
        print(f"Error: Path '{path}' does not exist")
        return False
    
    try:
        if os.path.isfile(path):
            os.remove(path)
            print(f"Successfully deleted file: {os.path.basename(path)}")
        elif os.path.isdir(path):
            shutil.rmtree(path)
            print(f"Successfully deleted folder: {os.path.basename(path)}")
        return True
    except Exception as e:
        print(f"Error deleting: {e}")
        return False


def main_menu():
    """Display main menu and handle user choice"""
    while True:
        print("\n" + "=" * 50)
        print("MAIN MENU")
        print("=" * 50)
        print("1. Move files by extension")
        print("2. Move entire folder")
        print("3. Delete permanently")
        print("4. Exit")
        print("=" * 50)
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            handle_move_files()
        elif choice == '2':
            handle_move_folder()
        elif choice == '3':
            handle_delete_permanently()
        elif choice == '4':
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


def handle_move_files():
    """Handle moving files by extension"""
    print("\n--- MOVE FILES BY EXTENSION ---")
    
    source = get_directory("Select SOURCE directory (where files are located)")
    dest = get_directory("Select DESTINATION directory (where to move files)")
    
    print(f"\nSource: {source}")
    print(f"Destination: {dest}")
    
    if not confirm_action("Are these directories correct?"):
        return
    
    extensions = get_extensions()
    if not extensions:
        print("No extensions specified. Returning to main menu.")
        return
    
    print(f"\nWill move files with extensions: {', '.join(f'.{ext}' for ext in extensions)}")
    print(f"From: {source}")
    print(f"To: {dest}")
    
    if confirm_action("Proceed with moving files?"):
        move_files_by_extension(source, dest, extensions)


def handle_move_folder():
    """Handle moving entire folder"""
    print("\n--- MOVE ENTIRE FOLDER ---")
    
    source = get_directory("Select FOLDER to move")
    dest = get_directory("Select DESTINATION directory")
    
    print(f"\nFolder to move: {source}")
    print(f"Destination: {dest}")
    
    if confirm_action("Move this folder?"):
        move_folder(source, dest)


def handle_delete_permanently():
    """Handle permanently deleting items"""
    print("\n--- DELETE PERMANENTLY ---")
    print("WARNING: This will permanently delete files/folders!")
    
    path = get_directory("Select file or folder to delete permanently")
    
    print(f"\nWill permanently delete: {path}")
    print("This action cannot be undone!")
    
    if confirm_action("Are you absolutely sure you want to delete this?"):
        if confirm_action("Final confirmation - DELETE PERMANENTLY?"):
            delete_permanently(path)


def main():
    """Main program entry point"""
    try:
        show_banner()
        main_menu()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()