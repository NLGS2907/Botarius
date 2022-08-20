"""
Events Cog.
"""

from typing import TYPE_CHECKING

from discord import Guild
from discord.ext.commands import Cog, Context

from ..db import fetch_records_from_table, insert_records_into_table
from ..db.shortcuts import register_guild, get_default_prefix
from .general import GeneralCog

if TYPE_CHECKING:

    from ..botarius import Botarius


class EventsCog(GeneralCog):
    """
    Cog for events.
    """

    @Cog.listener()
    async def on_ready(self) -> None:
        """
        ElBotarius is on and ready to use.
        """

        self.bot.log.info(f"{self.bot.user} is connected and ready to use!")

    @Cog.listener()
    async def on_command(self, ctx: Context):
        """
        The user is invoking a command.
        """

        self.bot.log.info(f"The user {ctx.author} is trying to invoke '{ctx.command}' on the " +
                          f"channel '#{ctx.channel.name}' of guild '{ctx.guild.name}'. " +
                          f"The message is '{ctx.message.content}'.")

    @Cog.listener()
    async def on_command_completion(self, ctx: Context):
        """
        The user invoked a command satisfactorily.
        """

        self.bot.log.info(f"{ctx.author} has invoked '{ctx.command}' satisfactorily")


    @Cog.listener()
    async def on_guild_join(self, guild: Guild) -> None:
        """
        Botarius connected to a guild for the first time.
        """

        self.bot.log.info(f"Botarius has connected to guild '{guild.name}'.")
        exists_in_db = fetch_records_from_table("guild_prefixes",
                                                guild_id=guild.id)

        if not exists_in_db:
            register_guild(guild.id, guild.name)


async def setup(bot: "Botarius"):
    """
    Adds this cog to botarius.
    """

    await bot.add_cog(EventsCog(bot))
