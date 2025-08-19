
'''This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.'''


import os
import shutil
import argparse
import sys
from pathlib import Path
import winshell
import ctypes

def cli_commands():
    parser = argparse.ArgumentParser(description="These are the current commands for the program to function.")
    parser.add_argument("-mf", "--move-folder", nargs=2, metavar=("SRC","DEST"), help="Move a folder from Source to Destination")
    parser.add_argument("-er", "--empty-recycle", action="store_true",help="This command will empty the recycle bin on Windows systems.")
    parser.add_argument("-ed","--empty-downloads", action="store_true", help="This command will empty the download folders on Windows systems.")
    return parser

#This function will log activity to a .txt file for the user to review anytime that they want or need.
def activity_logger():
    log = open ("activity.txt", "a")
    print("Coming soon!")


def show_banner():

    """Display program banner"""
    print("=" * 60)
    print("         Open File Mover CLI")
    print("         Version 1.0.1-Beta-Prerelease")
    print("=" * 60)
    print()

# For security practices we should make sure that the program is run as a Admin.

def confirm_admin_mode():
    if ctypes.windll.shell32.IsUserAnAdmin() == True:
        return True;
    else:
        return False;

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

def empty_recycle():
    try:
        winshell.recycle_bin().empty(confirm=False, show_progress=True, sound=True)
        print("Success!")
    except:
        print("Your recycle bin is already empty.")

def empty_downloads():
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

    if not os.path.exists(downloads_path):
        print("Downloads folder does not exist")
        return

    # Iterate through all items in the Downloads folder
    for item in os.listdir(downloads_path):
        item_path = os.path.join(downloads_path, item)
        try:
            # If it's a file, delete it
            if os.path.isfile(item_path):
                os.remove(item_path)
                print(f"Deleted file: {item}")
            # If it's a directory, delete it recursively
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Deleted directory: {item}")
        except PermissionError:
            print(f"Permission denied: Could not delete {item}")
        except Exception as e:
            print(f"Error deleting {item}: {e}")

    print("Downloads folder emptied successfully.")



def main():
    try:
        adminMode = confirm_admin_mode()
        if adminMode == True:
            show_banner()
            parser = cli_commands()
            args = parser.parse_args()
            if args.move_folder:
                Source, Destination = args.move_folder
                move_folder(Source,Destination)

            if args.empty_recycle:
                empty_recycle()
            if args.empty_downloads:
                empty_downloads()
            if not any(vars(args).values()):
                parser.print_help()
                exit()

        else:
            print("ERROR: Oops! This project needs superpowers to run. Please launch it as an administrator to unlock its full potential!")
            print("EXITING!")

    except TypeError:
        print("Please run --help or read the documentation on our github for troubleshooting.")
        print("EXITING!")



if __name__ == "__main__":
    main()
