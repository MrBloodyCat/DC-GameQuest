import disnake
from disnake.ext import commands
from .cleaning import CleanCommand



def setup(bot: commands.Bot):
    bot.add_cog(CleanCommand(bot))
