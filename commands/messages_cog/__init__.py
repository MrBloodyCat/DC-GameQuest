from disnake.ext import commands
from .responder import DMResponder
from .greeting import GreetingResponder
from .handler import WelcomeHandler
from .promo import AutoPromo


def setup(bot: commands.Bot):
    bot.add_cog(DMResponder(bot))
    bot.add_cog(GreetingResponder(bot))
    bot.add_cog(WelcomeHandler(bot))
    bot.add_cog(AutoPromo(bot))
