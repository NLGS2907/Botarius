"""
Events Cog.
"""

from typing import TYPE_CHECKING

from discord import Guild
from discord.ext.commands import Cog, Context

from ..constants import DEFAULT_PREFIX, PROPERTIES_PATH
from ..files import load_json, save_json
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

        properties = load_json(PROPERTIES_PATH)
        properties["prefixes"][str(guild.id)] = DEFAULT_PREFIX
        save_json(properties, PROPERTIES_PATH)



async def setup(bot: "Botarius"):
    """
    Adds this cog to botarius.
    """

    await bot.add_cog(EventsCog(bot))
