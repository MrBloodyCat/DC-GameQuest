import disnake
from disnake.ext import commands

class TextCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="текст", description="Отправляет заранее заданный текст.")
    async def send_text(self, inter: disnake.AppCmdInter):
        await inter.response.send_message("👋 Добро пожаловать на сервер Game Quest!\nСледите за новостями и оставайтесь с нами!")
