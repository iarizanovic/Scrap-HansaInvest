######################################################
# Author: Ivan Arizanovic <ivanarizanovic@yahoo.com> #
######################################################

import os
import time
from config import debug_mode


def create_parents(path: str) -> None:
    """
    Create parent folders of specified path with parameter 'path'.
    """
    # Check if path is empty
    if not path:
        error_output(f"Parent directory '{path}' cannot be created")

    # Get parent folder, if path points to file
    if path.count("\\") and path[-1] != '\\':
        path = path[0:path.rfind("\\")]

    # Create missing parent folders
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except:
            error_output(f"Parent directory '{path}' cannot be created")


def info_output(msg: str) -> None:
    """
    Print specified message, but only if debug_mode is enabled in config file.
    :param msg: Message which will be printed
    """
    if debug_mode:
        print(f"{time.strftime('%Y-%d-%m %H:%M:%S')}: {msg}")


def warning_output(msg: str) -> None:
    """
    Print warning message, but only if debug_mode is enabled in config file.
    :param msg: Message which will be printed
    """
    if debug_mode:
        print(f"{time.strftime('%Y-%d-%m %H:%M:%S')}: \x1b[1;33mWarning: {msg}\x1b[0m")  # Yellow


def error_output(msg: str) -> None:
    """
    Print error message and exit the program.
    :param msg: Message which will be printed
    """
    if debug_mode:
        print(f"{time.strftime('%Y-%d-%m %H:%M:%S')}: \x1b[1;31mError: {msg}\x1b[0m")  # Red
    else:
        print(f"\x1b[1;31mError: {msg}\x1b[0m")  # Red

    # Exit the program
    exit(-1)
