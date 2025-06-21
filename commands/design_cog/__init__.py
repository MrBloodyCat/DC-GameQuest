from disnake.ext import commands
from .avatar import AvatarCommands
from .banner import BannerCommands

def setup(bot: commands.Bot):
    bot.add_cog(AvatarCommands(bot))
    bot.add_cog(BannerCommands(bot))


