
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
from datetime import datetime
from pathlib import Path
from art import *


LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_FILE = LOG_DIR / "activity.txt"

def log_activity(message: str):
    """Append activity to log file with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"[{timestamp}] {message}\n")

def cli_commands():
    parser = argparse.ArgumentParser(description="These are the current commands for the program to function.")
    parser.add_argument("-mf", "--move-folder", nargs=2, metavar=("SRC","DEST"), help="Move a folder from Source to Destination")
    parser.add_argument("-er", "--empty-recycle", action="store_true",help="This command will empty the recycle bin on Windows systems.")
    parser.add_argument("-ed","--empty-downloads", action="store_true", help="This command will empty the download folders on Windows systems.")
    return parser

def show_banner():
    """Print a cute banner for Open File Mover (standard library only)."""
    # Enable ANSI colors on Windows
    if os.name == "nt":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            mode = ctypes.c_uint()
            if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                kernel32.SetConsoleMode(handle, mode.value | 0x0004)
        except Exception:
            pass

    # Colors
    use_color = sys.stdout.isatty()
    RST   = "\033[0m" if use_color else ""
    BOLD  = "\033[1m" if use_color else ""
    DIM   = "\033[2m" if use_color else ""
    PINK  = "\033[95m" if use_color else ""
    CYAN  = "\033[96m" if use_color else ""
    GREEN = "\033[92m" if use_color else ""
    YELLOW= "\033[93m" if use_color else ""
    WHITE = "\033[97m" if use_color else ""

    # Glyphs
    ascii_only = bool(os.environ.get("OFM_ASCII", ""))
    if ascii_only:
        TL, TR, BL, BR, H, V = "+", "+", "+", "+", "-", "|"
        icon_left, icon_right, spark = "[DIR]", "[MOVE]", "*"
    else:
        TL, TR, BL, BR, H, V = "╭", "╮", "╰", "╯", "─", "│"
        icon_left, icon_right, spark = "📂", "🚚", "✦"

    # Width
    width = shutil.get_terminal_size((80, 20)).columns
    inner = max(48, min(100, width - 4))

    def center(text): return text.strip().center(inner)

    # Lines
    top    = f"{TL}{H * (inner + 2)}{TR}"
    title  = f"{V} {center(f'{BOLD}{PINK}{icon_left}  Open File Mover  {icon_right}{RST}')} {V}"
    sub    = f"{V} {center(f'{CYAN}{spark} CLI utility for moving files ✨{RST}')} {V}"
    usage  = f"{V} {center(f'{GREEN}Version:{RST} {WHITE}1.0.1-Beta{RST}')} {V}"
    hint   = f"{V} {center(f'{DIM}{YELLOW}Tip:{RST}{DIM} use --help for options{RST}')} {V}"
    bottom = f"{BL}{H * (inner + 2)}{BR}"

    print()
    print(top)
    print(title)
    print(sub)
    print(usage)
    print(hint)
    print(bottom)
    print()


# For security practices we should make sure that the program is run as a Admin.
def confirm_admin_mode():
    if ctypes.windll.shell32.IsUserAnAdmin() == True:
        return True
    else:
        return False

def move_folder(source_dir, dest_dir):
    """Move entire folder from source to destination"""
    source_path = Path(source_dir)
    dest_path = Path(dest_dir)

    if not source_path.exists():
        msg = f"Error: Source directory '{source_dir}' does not exist"
        print(msg)
        log_activity(msg)
        return False

    if not dest_path.exists():
        msg = f"Error: Destination directory '{dest_dir}' does not exist"
        print(msg)
        log_activity(msg)
        return False

    folder_name = source_path.name
    final_dest = dest_path / folder_name

    try:
        shutil.move(str(source_path), str(final_dest))
        msg = f"Successfully moved folder '{folder_name}' to '{dest_dir}'"
        print(msg)
        log_activity(msg)
        return True
    except Exception as e:
        msg = f"Error moving folder '{source_dir}' → '{dest_dir}': {e}"
        print(msg)
        log_activity(msg)
        return False

def empty_recycle():
    try:
        winshell.recycle_bin().empty(confirm=False, show_progress=True, sound=True)
        msg = "Recycle bin emptied successfully."
        print(msg)
        log_activity(msg)
    except:
        msg = "Recycle bin already empty or error occurred."
        print(msg)
        log_activity(msg)

def empty_downloads():
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

    if not os.path.exists(downloads_path):
        msg = "Downloads folder does not exist"
        print(msg)
        log_activity(msg)
        return

    deleted_items = []
    for item in os.listdir(downloads_path):
        item_path = os.path.join(downloads_path, item)
        try:
            if os.path.isfile(item_path):
                os.remove(item_path)
                deleted_items.append(f"Deleted file: {item}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                deleted_items.append(f"Deleted directory: {item}")
        except PermissionError:
            deleted_items.append(f"Permission denied: Could not delete {item}")
        except Exception as e:
            deleted_items.append(f"Error deleting {item}: {e}")

    for entry in deleted_items:
        print(entry)
        log_activity(entry)

    msg = "Downloads folder emptied successfully."
    print(msg)
    log_activity(msg)

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
            msg = "ERROR: Please run this program as Administrator!"
            print(msg)
            log_activity(msg)
            print("EXITING!")

    except TypeError:
        msg = "TypeError occurred: Please run --help or check documentation."
        print(msg)
        log_activity(msg)
        print("EXITING!")

if __name__ == "__main__":
    main()
