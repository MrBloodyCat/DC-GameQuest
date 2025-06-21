from disnake.ext import commands
from .integration import IntegrationAnnouncer



def setup(bot: commands.Bot):
    bot.add_cog(IntegrationAnnouncer(bot))
