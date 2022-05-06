"""
Files management functions Module.
"""

from json import dump, load
from os import listdir
from typing import Dict, List, Optional

PairsDict = Dict[str, str]


def load_json(file_name: str) -> PairsDict:
    """
    Reads and loads a JSON file.
    """
    pairs_dict = {}

    with open(file_name, mode='r', encoding="utf-8") as file:
        pairs_dict = load(file)

    return pairs_dict


def save_json(pairs_dict: PairsDict, file_name: str, indent: int=4) -> None:
    """
    Receives a dictionary and dumps its information into a JSON file.
    """
    with open(file_name, mode='w', encoding="utf-8") as file:
        dump(pairs_dict, file, indent=indent)


def files_list(path: str, ext: Optional[str]=None) -> List[str]:
    """
    Searches the specified path for files, and returns a list with such files' names.

    If `ext` is not `None`, then it will look for files with that extension.
    `ext` must NOT have a leading dot (`.`), meaning that `"py"` will be automatically
    treated as `.py`.
    """

    return [file for file in listdir(path) if (file.endswith(f".{ext}") if ext else True)]
