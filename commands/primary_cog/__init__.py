import disnake
from disnake.ext import commands
from .memory import MemoryCleaner


def setup(bot: commands.Bot):
    bot.add_cog(MemoryCleaner(bot))