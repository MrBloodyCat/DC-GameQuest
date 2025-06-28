from disnake.ext import commands
from .bot import BotBan



def setup(bot: commands.Bot):
    bot.add_cog(BotBan(bot))
