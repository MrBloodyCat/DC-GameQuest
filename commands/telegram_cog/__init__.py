from disnake.ext import commands
from .posts import TelegramBridge


def setup(bot: commands.Bot):
    bot.add_cog(TelegramBridge(bot))
