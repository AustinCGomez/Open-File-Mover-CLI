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
VERSION = "Version 0.4.0.0-Discontinued"
LICENSE = "Project published under the Unlicense License and dedicated to the public domain."




''' The purpose of our view class is retrieve the input and output data that the user is requesting and then to be able to send it to our controller class for further analyzies'''
class Views():
    def __init__(self, directory_from, directory_to):
        self.directory_from = directory_from
        self.directory_to = directory_to
        self.extension_list = []


    def retrieve_directories_view(self):
        print("A small window will open on your screen in the next few seconds which will allow you to pick your source directory.")
        self.directory_from = filedialog.askdirectory()
        print("A small window will open on your screen in the next few seconds which will allow you to pick your destination directory.")
        self.directory_to = filedialog.askdirectory()
        print("Source Directory:", self.directory_from)
        print("Destination Directory:", self.directory_to)
        click.echo("Are the chosen directories correct?")
        action = click.prompt(
        "-y - Yes, directories are correct.\n"
        "-n - No, directories are not correct",
        type = click.Choice(['-y', '-n'])
        )

        if action == "-y".lower():
            print("Initializing...")
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
        print("-" * 130)
        sys.exit()

    def move_files_output(self, fileName, dir_a, dir_b):
        output_padding = " " * (len("Name") - len("Extension"))
        print(" ")
        print(f"Name: {fileName}{output_padding} - Removed From: {dir_a} and moved to: {dir_b}")
        print(" ")

    def move_folders_output(self, dir_a, dir_b):
        print(f"SUCCESS: The Folder has been moved from {dir_a} to {dir_b}")

''' The purpose of our controller class is to handle the logic that is sent from our view and then process what needs to be sent to the model to run specific programs.'''
class Controller():
    def __init__(self, dir_a, dir_b, ExtList):
        self.dir_a = dir_a
        self.dir_b = dir_b
        self.ExtList = ExtList

    def view_instances(self, decision):

        ViewChoices = Views(self.dir_a, self.dir_b)
        # 1 = flag for ending program view.
        if decision == 1:
            ViewChoices.end_program_view()
        # 2 = flag for retreiving the directories view.
        elif decision == 2:
            self.directory_value_a = None
            self.directory_value_b = None
            dir_a, dir_b = ViewChoices.retrieve_directories_view()
            self.directory_value_a = dir_a
            self.directory_value_b = dir_b
            return self.directory_value_a, self.directory_value_b
        # 3 = flag for retreve_extensions_view
        elif decision == 3:
            self.mylist = []
            mylist = ViewChoices.retrieve_extensions_view(self.mylist)
            self.mylist = mylist
        elif decision == 4:
            ViewChoices.retrieve_just_one_directory_view()
            

            
    def model_instances(self, decision):

        ModelChoices = Model(self.dir_a, self.dir_b, self.ExtList)
        #1 = flag for moving the files to trash through Move2Trash
        if decision == 1:
            ModelChoices.move_2trash_command()
        #2 = flag for moving files to another destination.
        elif decision == 2:
            ModelChoices.move_files_command()
        #3 = flag for moving folders to another destination.
        elif decision == 3:
            ModelChoices.move_folders_command()



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
            self.view_instances(1)


    def move_files_by_extension(self):
        directory_a = None
        directory_b = None
        #Retrieve the files by extension.
        directory_a, directory_b = self.view_instances(2)
        
        self.dir_a = directory_a  #Updating our instance variable from our view for the source directory.
        self.dir_b = directory_b  #updating our instance variable from our view for the destination directory.
        print("dir_a is source", directory_a)
        print("dir_b is destination", directory_b)
        self.view_instances(3)
        self.model_instances(2)

    # Move this to a function in the views eventually.
    def error_extensions(self):
        print(f'{self.ExtList} extension not found in directory {self.dir_a}. Please reenter the extension names.\n')
        print(" ")

    def move_folders_1_by_1(self):
        directory_a = None
        directory_b = None
        directory_a, directory_b = self.view_instances(2)
        self.dir_a = directory_a  #Updating our instance variable from our view for the source directory.
        self.dir_b = directory_b  #updating our instance variable from our view for the destination directory.
        self.model_instances(3)
    
    def move_folder_2_trash(self):
        self.directory_a = None
        self.directory_b = None
        self.view_instances(3)
        self.model_instances(1)

    def relay_error_message(self):
        print("Fatal error has occured when attempting to move your folder to the trash. Please screenshot this and open a issue on our github.")
        print(" ")
        print("Sending you back to the main menu.. sorry about that. :( )")
        self.command_line_options()

        

class Model():
    def __init__(self, dir_a, dir_b, ExtList):
        self.dir_a = dir_a
        self.dir_b = dir_b
        self.ExtList = ExtList
    
    def view_instances(self,decision, fileName):
        InstanceView = Views(self.dir_a, self.dir_b)
        if decision == 1:
            InstanceView.move_files_output(self.dir_a, self.dir_b)
        elif decision == 2: 
            InstanceView.move_files_output(fileName, self.dir_a, self.dir_b)
        elif decision ==3:
            InstanceView.move_folders_output(self.dir_a, self.dir_b)


    

    def controller_instances(self, decision):
        command_line_options = Controller(self.dir_a, self.dir_b, self.ExtList)
        if decision == 1:
            command_line_options.command_line_options()
        elif decision == 2: 
            command_line_options.relay_error_message()
        elif decision == 3:
            command_line_options.relay_error_message()
        elif decision == 4:
            command_line_options.error_extensions()

    
    
    def call_foldermove_method(self):
        MovedFolder = Views(self.dir_a, self.dir_b)
        MovedFolder.move_folders_output(self.dir_a, self.dir_b)
    
    def filemoving_methods(self, decision, file):
        #1 = We will instance View class for the move_files_output function.
        FileMethods = Views(self.dir_a, self.dir_b)
        if decision == 1:
            # We are sending the FileName, Directory 1, and Directory 2 to the View.
            FileMethods.move_files_output(FileName, dir_a, dir_b)



    def move_files_command(self):
        try:
            output_padding = " " * (len("Name") - len("Extension"))
            normalized_extensions = [ext.lower() for ext in self.ExtList]
            from_file_ext = [os.path.splitext(file)[-1].lstrip('.').lower() for file in os.listdir(self.dir_a)]
            for ext in normalized_extensions:
                if ext not in from_file_ext:
                    time.sleep(2)
                    #Displaying error message for the instance.
                    self.controller_instances(4)
                    break
            for file in os.listdir(self.dir_a):
                if any(file.lower().endswith(ext) for ext in normalized_extensions):
                    src_path = os.path.join(self.dir_a, file)
                    dest_path = os.path.join(self.dir_b, file)
                    shutil.move(src_path, dest_path)
                self.view_instances(2,file)
        except NameError:
            self.controller_instances(2)

         

    def move_folders_command(self):
        try:
            shutil.move(self.dir_a, self.dir_b)
        except NameError:
            self.controller_instances(3)
                
    def move_2trash_command(self):
        try:
            send2trash.send2trash(self.dir_a)
        except:
            self.controller_instances(3)

if __name__ == "__main__":
    dir_a = None
    dir_b = None
    ext = None
    BeginProgram = Controller(dir_a, dir_b, ext)
    BeginProgram.command_line_options()
