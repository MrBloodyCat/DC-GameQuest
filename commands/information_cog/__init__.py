import disnake
from disnake.ext import commands
from .server import ServerInfo



def setup(bot: commands.Bot):
    bot.add_cog(ServerInfo(bot))
    