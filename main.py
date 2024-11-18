'''
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


import os
import sys
import shutil
import typer
import time
from tkinter import filedialog
from tkinter import *
import click
from art import *
import send2trash

''' Static functions that give some information about our program'''
LOGO = text2art("Python File Mover")
GOODBYE = text2art("GOODBYE")
CONTRIBUTE = ("Want additional features? Spotted a bug? Head to our Github and lend a helping hand :) ->  https://github.com/AustinCGomez/Python-File-Mover-CLI")
VERSION = "Version 0.4.0."
LICENSE = "Project published under the Unlicense License and dedicated to the public domain."




'''The view class will contain all of our logic for what is visually seen to the user. '''
class Views():
    def __init__(self, directory_from, directory_to):
        self.dir_a = directory_from
        self.dir_b = directory_to
        self.extension_list = []
    # The main menu view will contain the structing for the first introduction that the user has to thew application.

    def default_statements():
        #Controller will send us a code that then invokes a default statement in one of our views.
        print("HI")

# The purpose of this function is to retrieve the directories from the user. 
    def retrieve_directories_view(self):
        print("A small window will open on your screen in the next few seconds which will allow you to pick your source directory.")
        time.sleep(2)
        self.directory_from = filedialog.askdirectory()
        print("A small window will open on your screen in the next few seconds which will allow you to pick your destination directory.")
        self.directory_to = filedialog.askdirectory()
        time.sleep(2)
        print("Source Directory:", self.directory_from)
        print("Destination Directory:", self.directory_to)
        click.echo("Are the chosen directories correct?")
        action = click.prompt(
        "-y - Yes, directories are correct.\n"
        "-n - No, directories are not correct",
        type = click.Choice(['-y', '-n'])
        )

        if action == "-y".lower():
            print("Vertification complete...")
            time.sleep(1)
            print("Initializing...")
            time.sleep(1)
        elif action == "-n":
            print("We are going to reverify the direcotires as the next step.")

        return self.directory_from, self.directory_to

    def retrieve_just_one_directory_view(self):
        print("A small window will open on your screen in the next few seconds which will allow you to pick your source directory.")
        time.sleep(2)
        self.directory_from = filedialog.askdirectory()
        print("Chosen Directory: ", self.directory_from)
        click.echo("Is the chosen directory correct?")
        action = click.prompt(
        "-y - Yes, directories are correct.\n"
        "-n - No, directories are not correct",
        type = click.Choice(['-y', '-n'])
        )
        if action == "-y".lower():
            print("Vertification complete...")
            time.sleep(1)
            print("Initializing...")
            time.sleep(1)
        elif action == "-n":
            print("We are going to reverify the direcotires as the next step.")
        
        return self.directory_from

  
    def retrieve_extensions_view(self, extension_list):
        while True: 
            self.getInput = input("Please enter each file extension that you wish to move files from and when you are done please type 'complete'. ")
            
            if self.getInput == 'complete'.lower():
                break
            self.extension_list.append(self.getInput)

        return self.extension_list

    def start_program_view(self):
        print(LOGO)
        print(VERSION)
        print(LICENSE)

    def end_program_view(self):
        print("-" * 130)
        print(GOODBYE)
        print(CONTRIBUTE)
        print(LICENSE)
        print(AUTHOR)
        print("-" * 130)
        sys.exit()




    def move_files_output(self, fileName, dir_a, dir_b):
        output_padding = " " * (len("Name") - len("Extension"))
        print(" ")
        print(f"Name: {fileName}{output_padding} - Removed From: {dir_a} and moved to: {dir_b}")
        print(" ")

    def move_folders_output(self, dir_a, dir_b):
        print(f"SUCCESS: The Folder has been moved from {self.dir_a} to {self.dir_b}")


class Controller():
    def __init__(self, dir_a, dir_b, ExtList):
        self.dir_a = dir_a
        self_dir_b = dir_b
        self.ExtList = ExtList
    def command_line_options(self):
        StartView = Views(dir_a, dir_b)
        StartView.start_program_view()
        print(" ")
        click.echo("Please choose an option from below: ")
        action = click.prompt(
        "-mfiles - Move files by specific file extension from Directory A to Directory B!\n"
        "-mfolders - Move Entire Folders from Directory A to Directory B!\n"
        "-mrecycle - Move file to the recycle bin!\n",
        "-quit - Exit out of the program\n",
        type = click.Choice(['-mfiles', '-mfolders', '-mrecycle', '-quit'])
        )

        if action == "-mfiles".lower():
            self.move_files_by_extension()
        elif action == "-mfolders":
            self.move_folders_1_by_1()
        elif action == '-mrecycle':
            self.move_folder_2_trash()
        elif action == '-quit':
            directoryA = None
            directoryB = None
            QuitProgram = Views(directoryA, directoryB)
            QuitProgram.end_program_view()

    def move_files_by_extension(self):
        self.directory_a = None 
        self.directory_b = None
        GetDirs = Views(self.directory_a, self.directory_b)
        directory_a, directory_b = GetDirs.retrieve_directories_view()
       
        self.directory_a = directory_a  #Updating our instance variable from our view for the source directory.
        self.directory_b = directory_b  #updating our instance variable from our view for the destination directory.


        # Invoking another method at this stage in our view to gather a list of extensions. 
        self.mylist = []
        mylist = GetDirs.retrieve_extensions_view(self.mylist)
        print("Let's check to see if mylist is populated", mylist)
        self.mylist = mylist # We are now saving our list with the important file extensions.
        # We will now ship our code to our model to handle the logic work for the operation and that information is going to be sent to our view. 
        MoveFilesCommand = Model(self.directory_a, self.directory_b, self.mylist)
        MoveFilesCommand.move_files_command()

    # Move this to a function in the views eventually.
    def error_extensions(self):
        print(f'{self.ExtList} extension not found in directory {self.dir_a}. Please reenter the extension names.\n')
        print(" ")

    def move_folders_1_by_1(self):
        self.directory_a = None 
        self.directory_b = None
        GetDirs = Views(self.directory_a, self.directory_b)
        directory_a, directory_b = GetDirs.retrieve_directories_view()
       
        self.directory_a = directory_a  #Updating our instance variable from our view for the source directory.
        self.directory_b = directory_b  #updating our instance variable from our view for the destination directory.

        # The next phase is to send the code over to our Model to process the logic aspect of the program.
        self.mylist = []
        MoveFoldersCommand = Model(self.directory_a, self.directory_b, self.mylist)
        MoveFoldersCommand.move_folders_command()
        SendBackController = Controller(self.directory_a, self.directory_b, self.ExtList)
        SendBackController.command_line_options()

    def move_folder_2_trash(self):
        self.directory_a = None
        self.directory_b = None
        GetDirs = Views(self.directory_a, self.directory_b)
        directory_to_trash = GetDirs.retrieve_just_one_directory_view()
        self.directory_a = directory_to_trash
        SendToTrash = Model(self.directory_a, self.directory_b, self.ExtList)
        SendToTrash.move_2trash_command()

    def error_exeption(self):
        print("Fatal error has occured when attempting to move your folder to the trash. Please screenshot this and open a issue on our github.")
        print(" ")
        print("Sending you back to the main menu.. sorry about that. :( )")
        self.command_line_options()
        time.sleep(1)

        

class Model():
    def __init__(self, dir_a, dir_b, ExtList):
        self.dir_a = dir_a
        self.dir_b = dir_b
        self.ExtList = ExtList
    def move_files_command(self):
        try: 
            output_padding = " " * (len("Name") - len("Extension"))
            # Normalize user extensions to lowercase
            normalized_extensions = [ext.lower() for ext in self.ExtList]
            # Check for files in the source directory
            from_file_ext = [os.path.splitext(file)[-1].lstrip('.').lower() for file in os.listdir(self.dir_a)]
            for ext in normalized_extensions:
                if ext not in from_file_ext:
                    ControllerError = Controller(self.dir_a, self.dir_b, self.ExtList)

                    ControllerError.error_extensions()
                    time.sleep(1)
                    break
            for file in os.listdir(self.dir_a):
                if any(file.lower().endswith(ext) for ext in normalized_extensions):  # Normalize case
                    src_path = os.path.join(self.dir_a, file)
                    dest_path = os.path.join(self.dir_b, file)
                    shutil.move(src_path, dest_path)
                # The model should not print anything out so we have to move this back to the controller somehow.
                FileStatus = Views(self.dir_a, self.dir_b)
                FileStatus.move_files_output(file,src_path, dest_path)
            SendBackController = Controller(self.dir_a, self.dir_b, self.ExtList)
            SendBackController.command_line_options()
        except:
            BackToMenu = Controller(self.dir_a, self.dir_b, self.ExtList)
            BackToMenu.error_exeption()

    def move_folders_command(self):
        try:
            shutil.move(self.dir_a, self.dir_b)
            MovedFolder = Views(self.dir_a, self.dir_b)
            MovedFolder.move_folders_output(self.dir_a, self.dir_b)
        except: 
            BackToMenu = Controller(self.dir_a, self.dir_b, self.ExtList)
            BackToMenu.error_exeption()

    
    def move_2trash_command(self):
        try:
            send2trash.send2trash(self.dir_a)
        except:
            BackToMenu = Controller(self.dir_a, self.dir_b, self.ExtList)
            BackToMenu.error_exeption()

if __name__ == "__main__":
    dir_a = None
    dir_b = None
    ext = None
    BeginProgram = Controller(dir_a, dir_b, ext)
    BeginProgram.command_line_options()
