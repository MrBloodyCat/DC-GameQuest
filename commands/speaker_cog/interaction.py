import os
import disnake
from disnake.ext import commands
from BANNED_FILES.config import SPEAKER_VOICE_ID, Music_Image, Embed_Color

class MusicIntegration(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.message: disnake.Message | None = None
        self.embed_image_filename = os.path.basename(Music_Image)
        self.embed_color = disnake.Color(int(Embed_Color.lstrip("#"), 16))

    def _clean_track_name(self, track_name: str) -> str:
        """Удаляем расширение файла из названия трека"""
        return os.path.splitext(track_name)[0]

    async def send_or_update_message(self, track_name: str):
        channel = self.bot.get_channel(SPEAKER_VOICE_ID)
        if channel is None:
            print("Канал не найден")
            return

        clean_name = self._clean_track_name(track_name)

        file = disnake.File(Music_Image, filename=self.embed_image_filename)

        embed = disnake.Embed(
            title="<:playlis:1385657627228377089> Сейчас в эфире — наш персональный хит!",
            description=f"Тот самый бит, от которого дрожат стёкла:\n> **{clean_name}**",
            color=self.embed_color
        )
        embed.set_image(url=f"attachment://{self.embed_image_filename}")
        embed.set_footer(
            text="Благодарим за проявленный интерес к нашему спецпроекту!"
        )

        if self.message is None:
            self.message = await channel.send(embed=embed, file=file)
        else:
            try:
                await self.message.edit(embed=embed)
            except disnake.NotFound:
                # Если сообщение удалили, отправляем заново
                self.message = await channel.send(embed=embed, file=file)

    async def delete_message(self):
        if self.message:
            try:
                await self.message.delete()
            except disnake.NotFound:
                pass
            self.message = None