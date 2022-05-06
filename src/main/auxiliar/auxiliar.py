"""
Auxiliar functions Module.
"""

from typing import TYPE_CHECKING

from discord import Message

from ..constants import PROPERTIES_PATH, DEFAULT_PREFIX
from ..files import load_json

if TYPE_CHECKING:

    from ..botarius import Botarius

def get_prefix(_bot: "Botarius", message: Message) -> str:
    """
    Looks into the prefixes dictionary and returns the one
    that coincides with the corresponding guild.
    """

    return load_json(PROPERTIES_PATH)["prefixes"].get(str(message.guild.id), DEFAULT_PREFIX)
