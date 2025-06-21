import disnake
from disnake.ext import commands
from .activity import StatusBot
from .server import ServerInfo
from .text import TextCommands
from .reaction import MentionResponse


def setup(bot: commands.Bot):
    bot.add_cog(StatusBot(bot))
    bot.add_cog(ServerInfo(bot))
    bot.add_cog(MentionResponse(bot))
    bot.add_cog(TextCommands(bot))
