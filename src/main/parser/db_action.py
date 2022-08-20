"""
Database Interactive Console Module.
"""

from argparse import Action
from sqlite3 import connect
from sys import stdout
from typing import TYPE_CHECKING, Any, List

from ..db import DEFAULT_DB

if TYPE_CHECKING:
    from argparse import ArgumentParser, Namespace

LINE_UP = "\033[1A"
LINE_CLEAR = "\x1b[2K"

class InteractiveDBConsole(Action):
    """
    Interactive console for issuing SQL commands.
    """

    def _erase_console_lines(self, script: List[str]) -> None:
        "Tries to erase console command lines."

        if not script:
            return

        script.pop()
        stdout.write(f"{LINE_UP}{LINE_CLEAR}" * 2)
        stdout.flush()


    def __call__(self,
                 _parser: "ArgumentParser",
                 _namespace: "Namespace",
                 _values: List[Any],
                 _option_string=None):
        "Launches the interactive console."

        sql_script = []

        try:
            while True:

                stdout.write("Issuing SQL commands...\n\n")

                # -- Start issuing commands --
                while True:
                    line = input()

                    if not line:
                        break
                    elif line == "-r":
                        self._erase_console_lines(sql_script)
                    else:
                        sql_script.append(line)

                with connect(DEFAULT_DB) as con:
                    con.executescript(' '.join(sql_script))
                # -- End issuing commands --

                cmd = input("\n>>> Another command? (y/n): ")
                if cmd.lower() != 'y':
                    break

        except KeyboardInterrupt:
            stdout.write("Operation Interrupted. Ignoring...")
