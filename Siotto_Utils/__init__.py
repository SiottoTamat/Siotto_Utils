"""
File_handler: A utility library for loading, validating, and saving Excel and CSV files.
Author: Andrea Siotto
"""

from .File_handler import (check_UTF_8, clean_filename, file_to_list,
                           list_to_file, read_csv, read_excel)
from .Json_handler import merge_jsons

__all__ = [
    "check_UTF_8",
    "read_excel",
    "read_csv",
    "file_to_list",
    "list_to_file",
    "clean_filename",
    "merge_jsons",
]

__author__ = "Andrea Siotto"
__version__ = "1.0"
__email__ = "siotto.public@gmail.com"
__status__ = "Development"
