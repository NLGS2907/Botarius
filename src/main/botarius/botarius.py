"""
Home Module for the customized bot class 'Botarius'.
"""

from platform import system
from typing import TYPE_CHECKING, Callable

from discord import Game, Intents, Message
from discord.ext.commands import Bot
from discord.utils import utcnow

from ..auxiliar import get_prefix
from ..db.shortcuts import get_bot_id, get_cogs_path
from ..files import files_list
from ..logger import BotLogger

if TYPE_CHECKING:

    from datetime import datetime, timedelta

try:
    from asyncio import WindowsSelectorEventLoopPolicy, set_event_loop_policy

    if system() == "Windows":
        set_event_loop_policy(WindowsSelectorEventLoopPolicy())

except ImportError:

    BotLogger().warning("Could not import 'WindowsSelectorEventLoopPolicy', " +
                           "probably due to this OS being Windows.")


class Botarius(Bot):
    """
    Class for customizing the 'Bot' class.
    """


    @staticmethod
    def botarius_intents() -> Intents:
        """
        Creates an `Intents` object specialized for Botarius.
        """

        intents = Intents.default()
        intents.message_content = True # pylint: disable=assigning-non-slot

        return intents


    def __init__(self,
                 cmd_prefix: Callable=get_prefix,
                 actividad=Game(name="/info"),
                 **opciones) -> None:
        """
        Initializes an instance of 'Botarius'.
        """

        super().__init__(cmd_prefix,
                         activity=actividad,
                         intents=Botarius.botarius_intents(),
                         application_id=get_bot_id(),
                         options=opciones)

        self.awaken_at: "datetime" = utcnow()
        "The exact moment in which botarius awakens."


    async def setup_hook(self) -> None:
        """
        Realizes some initial procedures.
        """

        ext = "py"

        for cog_name in files_list(get_cogs_path(), ext=ext):
            if cog_name == "__init__.py":
                continue

            await self.load_extension(f".{cog_name.removesuffix(f'.{ext}')}",
                                      package="src.main.cogs")

        await self.tree.sync()


    @property
    def log(self) -> BotLogger:
        """
        Returns Botarius' logger.
        """

        return BotLogger()


    @property
    def uptime(self) -> "timedelta":
        """
        Shows Botarius' uptime.
        """

        return utcnow() - self.awaken_at


    @staticmethod
    def is_last_message(msg: Message) -> bool:
        """
        Verifies if the message in cuestion is the last
        one sent in the channel.
        """

        return msg == msg.channel.last_message


    def is_bot_message(self, msg: Message) -> bool:
        """
        Verifies if a message was sent by Botarius.
        """

        return not self.is_last_message(msg) and msg.author == self.user


    def is_command_message(self, msg: Message) -> bool:
        """
        Verifies if the message in cuestion is one for invoking a command.
        """

        return ((not self.is_last_message(msg) and msg.content.startswith(get_prefix(self, msg)))
                or self.is_bot_message(msg))
