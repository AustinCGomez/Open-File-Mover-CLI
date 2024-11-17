# python_file_mover/__init__.py

# Import necessary modules, classes, or functions to make them accessible when the package is imported
from .file_mover import GatherDirectoriesProcess, ObtainFileExtensionListProcess, EndProgramProcess, DefineCommands, MoveFilesCommand, MoveFoldersCommand, MoveFilesToTrashCommand

# Define what will be imported when using 'from python_file_mover import *'
__all__ = [
    'GatherDirectoriesProcess',
    'ObtainFileExtensionListProcess',
    'EndProgramProcess',
    'DefineCommands',
    'MoveFilesCommand',
    'MoveFoldersCommand',
    'MoveFilesToTrashCommand',
]
