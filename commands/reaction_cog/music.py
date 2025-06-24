import disnake
from disnake.ext import commands
from BANNED_FILES.config import SPEAKER_VOICE_ID, Musical_Reaction  

class ReactionMusic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_channel_id = SPEAKER_VOICE_ID
        self.emoji_ids = Musical_Reaction

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.channel.id != self.target_channel_id:
            return

        # Реагирует на все сообщения, включая сообщения бота
        for emoji_id in self.emoji_ids:
            emoji = self.bot.get_emoji(emoji_id)
            if emoji:
                try:
                    await message.add_reaction(emoji)
                except disnake.HTTPException:
                    print(f"Не удалось добавить реакцию: {emoji}")
            else:
                print(f"Emoji с ID {emoji_id} не найден!")
