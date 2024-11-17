
'''
MIT LICENSE
Copyright (c) [2023] [Austin Christopher Galindo Gomez]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''



# This is a prototype of a new menu using Click
import os
import sys
import shutil
import typer
import time
from tkinter import filedialog
from tkinter import *
import click
import pytest
from art import *
from unittest.mock import *

''' Static functions that give some information about our program'''
LOGO = text2art("Python FIle Mover")
GOODBYE = text2art("GOODBYE")
CONTRIBUTE = ("Want additional features? Spotted a bug? Head to our Github and lend a helping hand :) ->  https://github.com/AustinCGomez/Python-File-Mover-CLI")
VERSION = "Version 0.3.0 Beta."
LICENSE = "This software is published under the MIT License."
AUTHOR = "Program designed and Authored by Austin Gomez."
WARNING = "!!WARNING!! This command will DELETE files from Directory A and move them to DIRECTORY B."

class GatherDirectoriesProcess():
    ''' We will use one class only to get our To and FROM directories since the program can use it for all functions.
        ALl of the code to get and verify the directories will be in this class only. Any other classes
        can therefore create an instance of it.  '''
    def __init__(self, directory_a, directory_b):
        self.directory_from = directory_a
        self.directory_to = directory_b
    def process_error_handling(self, error_reason):
        print(f"Please re-enter the directories so that they are not {error_reason}")
    def obtain_dirs(self):
        print("Please select two directories from your computer system!")
        time.sleep(5)
        self.directory_from = filedialog.askdirectory()
        self.directory_to = filedialog.askdirectory()
        while not self.directory_from:
            self.directory_from = filedialog.askdirectory()
            if not self.directory_from:
                print("Error: Please define an FROM directory.")
        while not self.directory_to:
            self.directory_to = filedialog.askdirectory()
            if not self.directory_to:
                print("Error: Please define an TO directory.")

        if self.directory_from == self.directory_to:
            print("Error: Directory TO and Directory FROM cannot be the same!")
            self.obtain_dirs()

class ObtainFileExtensionListProcess():
    '''This service process will obtain our file extension list which will then be sent
    back to the MoveFileCommand() to be utilized for the operation of moving files by extension. '''
    def __init__(self, user_list=None):
        self.extension_list = []
        self.root = Tk()
    def obtain_file_list(self):
        while True:
            self.getInput = input("Please enter each file extension that you want to move files from | Type 'quit' when done.")

            if self.getInput == 'quit':
                break

            self.extension_list.append(self.getInput)

            print("List of user entered file extensions: ")

        return self.extension_list

class EndProgramProcess():
    '''This command will end the program when invoked. It's made into its class so that an instance can be made quickly from any
    class and therefore less code has to be written over and over again to end the program. '''
    def __init__(self):
        self.EndProgram = None
    def end(self):
        print("-" * 130)
        print(GOODBYE)
        print(CONTRIBUTE)
        print(LICENSE)
        print(AUTHOR)
        print("-" * 130)
        time.sleep(2)
        sys.exit()

class DefineCommands():
    ''' This class displays all of our classes and allows the user to select what actions they want to take '''
    def __init__(self):
        self.directory_from = None
        self.directory_to = None
    def main(self):
        print(LOGO)
        print(VERSION)
        print(LICENSE)
        print(" ")
        click.echo("Please choose the obtain below to begin: ")
        action = click.prompt(
        "--move-files - Move files by specific file extension from Directory A to Directory B!\n"
        "--move-folders - Move Entire Folders from Directory A to Directory B!\n"
        "--move-to-recycle - Move Entire Directory to the Windows Recycle Bin.",
        type = click.Choice(['--move-files', '--move-folders', '--move-to-recycle'])
        )

        if action == "--move-files":
            self.move_files_by_extension()
        elif action == "--move-folders":
            self.move_entire_folders()

    def move_files_by_extension(self):
        new_file_move = MoveFilesCommand(self.directory_from, self.directory_to)
        new_file_move.start_command()
        #go_to_move_command.start_command(blank_dir_a, blank_dir_b)

    def move_entire_folders(self):
        #Create a new instance in the #MoveFoldersCommand
        new_folder_move = MoveFoldersCommand(self.directory_from, self.directory_to)
        new_folder_move.process_file_move()




class MoveFilesCommand():

    def __init__(self, dir_a, dir_b):
        self.directory_from = None
        self.directory_to = None
        self.user_extensions = []

    def process_move(self):
        output_padding = " " * (len("Name") - len("Extension"))
        #Obtain extensions from our Extension Process first.
        click.echo("Please choose the obtain below to begin: ")
        action = click.prompt(
        "--begin - Begin the process of moving files first by obtaining a list of file extensions. B\n"
        "--quit - Quit the Move command and return to the main menu.",
        type = click.Choice(['--begin', '--quit'])
        )

        if action == "--begin":
            #create new instance to create file extension page.

            retrieve_file_extensions = ObtainFileExtensionListProcess(self.user_extensions)
            self.user_extensions = retrieve_file_extensions.obtain_file_list()
            print(" ")
            print("User Selected Extensions: ")
            print("--------------------------")
            for extension in self.user_extensions:
                print(extension)
            time.sleep(2)
            print("ATTEMPTING to move files based on extension from Directory A to Directory B")
            print(self.directory_from)
            print(self.directory_to)
            for file in os.listdir(self.directory_from):
                if any(file.endswith(ext) for ext in self.user_extensions):
                    src_path = os.path.join(self.directory_from, file)
                    dest_path = os.path.join(self.directory_to, file)
                    shutil.move(src_path, dest_path)
                    print(f"Name: {file}{output_padding} - Removed From: {src_path} and moved to: {dest_path}")
                    print(" ")



        elif action == "--quit":
            # Create a new instance invoking that the user wants to end the program.
            end_program = EndProgramProcess()
            EndProgramProcess.end(self.directory_from)


    def start_command(self):
        print(WARNING)
        print("Opening a Graphical User Interface(GUI) to obtain your directories to move files FROM A to B")
        # Create a new instance in Obtain_Directory to ensure that the directories arw what we want.
        verify_directories = GatherDirectoriesProcess(self.directory_from, self.directory_to)
        self.directory_from, self.directory_to = verify_directories.obtain_dirs()
        # Our input will be validated at this point and can be moved down the process line.
        self.process_move()


class MoveFoldersCommand():
    def __init__(self, dir_a, dir_b):
        self.directory_from = None
        self.directory_to = None
        self.user_extensions = []
    def process_file_move(self):
        print(WARNING)
        verify_directories = GatherDirectoriesProcess(self.directory_from, self.directory_to)
        self.directory_from, self.directory_to = verify_directories.obtain_dirs()
        shutil.move(self.directory_from, self.directory_to)
        print(f"SUCCESS: The Folder has been moved from {self.directory_from} to {self.directory_to}")


if __name__ == "__main__":
    BeginProgram = DefineCommands()
    BeginProgram.main()


'''Test case 1: Write a test to see what happens when Directory A and Directory B are set to the same directory by accident of the user in #GatherDirectoriesProcess.  '''
class TestGatherDirectoriesProcess():
    ''' We will use one class only to get our To and FROM directories since the program can use it for all functions.
        ALl of the code to get and verify the directories will be in this class only. Any other classes
        can therefore create an instance of it.  '''
    def test_obtain_dirs(self):
        root = Tk()
        root.withdraw()
        self.directory_from = filedialog.askdirectory()
        self.directory_to = filedialog.askdirectory()
        while not self.directory_from:
            print("error: ")
            self.directory_from = filedialog.askdirectory()
            if not self.directory_from:
                print("Error: Please define an FROM directory.")
        while not self.directory_to:
            self.directory_to = filedialog.askdirectory()
            if not self.directory_to:
                print("Error: Please define an TO directory.")
        if self.directory_from == self.directory_to:
            print("Error: Directory TO and Directory FROM cannot be the same!")
            self.test_obtain_dirs()

        assert self.directory_from != self.directory_to
        print(f"Obtained Directory A: {self.directory_from}")
        print(f"Obtained Directory B: {self.directory_to}")

        root.destroy()

        return self.directory_from, self.directory_to
