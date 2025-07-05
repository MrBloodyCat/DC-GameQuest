import disnake
from disnake.ext import commands
from .cleaning import CleanCommand
from .archive import AdsCommand


def setup(bot: commands.Bot):
    bot.add_cog(CleanCommand(bot))
    bot.add_cog(AdsCommand(bot))

