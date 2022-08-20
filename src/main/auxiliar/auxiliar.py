"""
Auxiliar functions Module.
"""

from argparse import ArgumentParser
from typing import TYPE_CHECKING

from discord import Message

from ..parser import InteractiveDBConsole
from ..db.shortcuts import get_guild_prefix

if TYPE_CHECKING:

    from ..botarius import Botarius

def get_prefix(_bot: "Botarius", message: Message) -> str:
    """
    Looks into the prefixes dictionary and returns the one
    that coincides with the corresponding guild.
    """

    return get_guild_prefix(guild_id=message.guild.id,
                            guild_name=message.guild.name)


def bot_args_parser() -> ArgumentParser:
    "Parses the arguments from a given array."

    parser = ArgumentParser(
        prog="Botarius",
        description="The Botarius discord bot."
    )

    opt = parser.add_argument_group("Optional",
                                    "Optional commands that may be issued for execution.")

    opt.add_argument("-d", "--database", nargs=0, action=InteractiveDBConsole)
    opt.add_argument("-v", "--version", action="version", version="Botarius v0.0.1")

    return parser
