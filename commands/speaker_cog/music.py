import os
import random
import asyncio
import subprocess
import disnake
from disnake.ext import commands, tasks
from BANNED_FILES.config import SPEAKER_VOICE_ID, Music_Folder #Ffmpeg_Path

class MusicPlayer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_client: disnake.VoiceClient | None = None
        self.music_folder = Music_Folder
        self.volume = 0.3
        #self.ffmpeg_path = Ffmpeg_Path
        self.integration_cog = None  # Для обращения к MusicIntegration
        self.auto_reconnect.start()

    async def connect_and_play(self):
        if self.integration_cog is None:
            self.integration_cog = self.bot.get_cog("MusicIntegration")

        voice_channel = self.bot.get_channel(SPEAKER_VOICE_ID)
        if not isinstance(voice_channel, disnake.VoiceChannel):
            print("Голосовой канал не найден или невалидный.")
            return

        try:
            if self.voice_client is None or not self.voice_client.is_connected():
                self.voice_client = await voice_channel.connect()
                if self.integration_cog:
                    await self.integration_cog.send_or_update_message("Ожидание пожалуста музыки...")
            elif self.voice_client.channel.id != voice_channel.id:
                await self.voice_client.move_to(voice_channel)
        except disnake.ClientException:
            return

        await asyncio.sleep(15)  # Задержка перед стартом

        files = [f for f in os.listdir(self.music_folder) if f.endswith((".mp3", ".wav", ".ogg", ".aac"))]
        if not files:
            print("Нет аудиофайлов для воспроизведения.")
            return

        while True:
            if not self.voice_client or not self.voice_client.is_connected():
                if self.integration_cog:
                    await self.integration_cog.delete_message()
                break

            file = random.choice(files)

            if self.integration_cog:
                await self.integration_cog.send_or_update_message(file)

            source = disnake.FFmpegPCMAudio(
                os.path.join(self.music_folder, file),
                #executable=self.ffmpeg_path,
                before_options='-hide_banner',
                options='-loglevel error',
                stderr=subprocess.DEVNULL
            )
            player = disnake.PCMVolumeTransformer(source, volume=self.volume)
            self.voice_client.play(player)

            while self.voice_client.is_playing() or self.voice_client.is_paused():
                await asyncio.sleep(1)

    @tasks.loop(seconds=35)
    async def auto_reconnect(self):
        voice_channel = self.bot.get_channel(SPEAKER_VOICE_ID)
        if not isinstance(voice_channel, disnake.VoiceChannel):
            return

        if self.voice_client is None or not self.voice_client.is_connected():
            if self.integration_cog:
                await self.integration_cog.delete_message()
            await self.connect_and_play()

    @auto_reconnect.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()


