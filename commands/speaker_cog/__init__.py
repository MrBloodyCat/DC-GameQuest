import disnake
from disnake.ext import commands
from .music import MusicPlayer
from .interaction import MusicIntegration


def setup(bot: commands.Bot):
    bot.add_cog(MusicPlayer(bot))
    bot.add_cog(MusicIntegration(bot))