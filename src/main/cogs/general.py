"""
General Cog, for inheritance use.
"""

from typing import TYPE_CHECKING

from discord.ext.commands import Cog

if TYPE_CHECKING:

    from ..botarius import Botarius


class GeneralCog(Cog):
    """
    A more general purpose Cog.
    """

    def __init__(self, bot: "Botarius") -> None:
        """
        Initializes an instance of 'GeneralCog'.
        """

        self.bot: "Botarius" = bot


async def setup(_bot: "Botarius"):
    """
    Adds this cog to botarius.
    This method should be overriden.
    """

    ...
