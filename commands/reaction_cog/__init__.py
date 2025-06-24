from disnake.ext import commands
from .music import ReactionMusic
from .youtube import ReactionYouTube
from .telegram import ReactionTelegram



def setup(bot: commands.Bot):
    bot.add_cog(ReactionMusic(bot))
    bot.add_cog(ReactionYouTube(bot))
    bot.add_cog(ReactionTelegram(bot))

