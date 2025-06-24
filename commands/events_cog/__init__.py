from disnake.ext import commands
from .voice import VoiceLogger
from .message import MessageLogger
from .role import RoleUpdateLogger
from .error import ErrorLogger


def setup(bot: commands.Bot):
    bot.add_cog(VoiceLogger(bot))
    bot.add_cog(MessageLogger(bot))
    bot.add_cog(RoleUpdateLogger(bot))
    bot.add_cog(ErrorLogger(bot))
