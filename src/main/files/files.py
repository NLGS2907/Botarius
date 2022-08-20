"""
Files management functions Module.
"""

from os import listdir
from typing import Dict, List, Optional

PairsDict = Dict[str, str]


def files_list(path: str, ext: Optional[str]=None) -> List[str]:
    """
    Searches the specified path for files, and returns a list with such files' names.

    If `ext` is not `None`, then it will look for files with that extension.
    `ext` must NOT have a leading dot (`.`), meaning that `"py"` will be automatically
    treated as `.py`.
    """

    return [file for file in listdir(path) if (file.endswith(f".{ext}") if ext else True)]
