"""
Admin commands Cog.
"""

from typing import TYPE_CHECKING

from discord.ext.commands import Context, command, is_owner

from ..constants import LOG_PATH, PROPERTIES_PATH
from ..files import load_json, save_json
from .general import GeneralCog

if TYPE_CHECKING:

    from ..botarius import Botarius


class AdminCog(GeneralCog):
    """
    Cog for admin commands.
    """

    @command(name="prefix",
             aliases=["prefijo", "pfx", "px"],
             usage="new_prefix",
             help="Changes the prefix for commands.")
    async def change_prefix(self, ctx: Context, new_prefix: str) -> None:
        """
        Changes the prefix used for invoking commands.

        It is assumed that the guild to be processed is already memorized in
        Botarius' data.
        """

        old_prefix = ctx.prefix

        properties = load_json(PROPERTIES_PATH)
        properties["prefixes"][str(ctx.guild.id)] = new_prefix
        save_json(properties, PROPERTIES_PATH)

        await ctx.channel.send(f"**[INFO]** The command prefix was changed from " +
                               f"`{old_prefix}` to `{new_prefix}` succesfully.",
                               delete_after=30.0)
        self.bot.log.info(f"The prefix in '{ctx.guild.name}' was changed from " +
                          f"{old_prefix} to {new_prefix} successfully.")


    @command(name="clear",
             aliases=["clean", "cls"],
             usage="limit [-full]",
             help="Cleans bot messages.")
    async def clear_messages(self, ctx: Context, limite: int, *options) -> None:
        """

        Clears all Botarius' messages, on the channel where the command
        was invoked from.

        If `-full` is among the options, it will also seek to delete the
        invocation messages of the users.
        """

        check_func = (self.bot.is_command_message
                      if "-full" in options
                      else self.bot.is_bot_message)
        purged = await ctx.channel.purge(limit=limite + 1, check=check_func)

        self.bot.log.info(f"{len(purged)} messages were eliminated from '#{ctx.channel.name}' " +
                          f"in guild '{ctx.guild.name}'.")

        await ctx.message.delete(delay=5.0)


    @command(name="shutdown",
             aliases=["shut", "exit", "quit", "salir"],
             help="Closes Botarius.",
             hidden=True)
    @is_owner()
    async def shutdown(self, ctx: Context) -> None:
        """
        Shuts down botarius.
        """

        self.bot.log.info(f"Closing {self.bot.user}...")
        await ctx.message.delete()
        await self.bot.close()


    @command(name="flush",
             aliases=["logclear", "logflush"],
             help="Empties log file.",
             hidden=True)
    @is_owner()
    async def logflush(self, ctx: Context):
        """
        Empties the log file contents.
        """

        with open(LOG_PATH, mode='w', encoding="utf-8"):

            await ctx.channel.send(f"**[INFO]** Emptying log file in `./{LOG_PATH}`...",
                                   delete_after=10.0)


    @command(name="uptime",
             aliases=["up_time"],
             help="Calculates Botarius' active time.",
             hidden=True)
    @is_owner()
    async def calculate_uptime(self, ctx: Context) -> None:
        """
        Calculates Botarius' active time.
        """

        delta = self.bot.uptime

        days = (f"`{delta.days}` día/s" if delta.days > 9 else "")

        possible_hours = (delta.seconds // 3600)
        hours = (f"`{possible_hours}` hora/s" if possible_hours > 0 else "")

        possible_minutes = (delta.seconds // 60)
        minutes = (f"`{possible_minutes}` minuto/s" if possible_minutes > 0 else "")

        possible_seconds = (delta.seconds % 60)
        seconds = (f"`{possible_seconds}` segundo/s" if possible_seconds > 0 else "")

        time = [tmp for tmp in [days, hours, minutes, seconds] if tmp]
        if len(time) > 1:
            last = time.pop()
            time[-1] = f"{time[-1]} y {last}"


        await ctx.message.delete()
        await ctx.channel.send(f"***{self.bot.user}** estuvo activo por {', '.join(time)}.*",
                               delete_after=20.0)


async def setup(bot: "Botarius"):
    """
    Adds this cog to botarius.
    """

    await bot.add_cog(AdminCog(bot))
