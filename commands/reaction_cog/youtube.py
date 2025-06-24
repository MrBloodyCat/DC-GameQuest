import disnake
from disnake.ext import commands
from BANNED_FILES.config import VIDEO_CHANNEL_ID, YouTube_Reaction  

class ReactionYouTube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_channel_id = VIDEO_CHANNEL_ID
        self.emoji_ids = YouTube_Reaction

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.channel.id == self.target_channel_id and not message.author.bot:
            for emoji_id in self.emoji_ids:
                emoji = self.bot.get_emoji(emoji_id)
                if emoji:
                    await message.add_reaction(emoji)
                else:
                    print(f"Emoji with ID {emoji_id} not found!")
