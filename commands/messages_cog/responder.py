import disnake 
from disnake.ext import commands
from BANNED_FILES.config import Community_Image, Embed_Color

class DMResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed_color = disnake.Color(int(Embed_Color.lstrip("#"), 16))

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot:
            return

        if isinstance(message.channel, disnake.DMChannel):
            file = disnake.File(Community_Image, filename="community.png")  # локальный файл с картинкой
            embed = disnake.Embed(
                title="<:aicomment:1385718618091819160> Штабное сообщение от Сержанта",
                description=(
                    ">>> Бот в данный момент **выполняет** боевую задачу на основном сервере. "
                    "Ответ временно невозможен, **благодарим** за понимание."
                ),
                color=self.embed_color
            )
            embed.add_field(
                name="<:aitag:1385718639805599824> Цель операции:",
                value="[Присоединиться к серверу](https://discord.gg/nQGvVAEw5r)",
                inline=False
            )
            embed.set_image(url="attachment://community.png")  # Крупное изображение внизу эмбеда
            embed.set_footer(text="Благодарим за проявленный интерес к нашему спецпроекту!")

            await message.channel.send(embed=embed, file=file)


