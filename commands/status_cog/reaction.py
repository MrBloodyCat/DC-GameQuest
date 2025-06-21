import disnake
from disnake.ext import commands
from BANNED_FILES.config import Embed_Color

class MentionResponse(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.embed_color = disnake.Color(int(Embed_Color.lstrip("#"), 16))

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot:
            return  # Игнорируем сообщения от других ботов

        # Проверяем, упомянут ли бот в сообщении
        if self.bot.user.mentioned_in(message):
            latency = round(self.bot.latency * 1000)  # Пинг в миллисекундах

            embed = disnake.Embed(
                title=f"<:airdrop:1385690982170886214> Штаб зафиксировал ваше имя — {message.author.display_name}!",
                description=(
                    "Здравия желаю! Я здесь и всегда готов **помочь** и внести вклад в проект **Game Quest**.\n\n"
                    f">>> Мой военный пинг принятен: {latency} мс.\n"
                    "Мои создатели: <@768782555171782667> и <@787093771115692062>\n"
                    "Website Muhameda: [muhamedlabs.pro](https://muhamedlabs.pro)"
                ),
                color=self.embed_color
            )
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(text="Благодарим за проявленный интерес к нашему спецпроекту!")

            await message.channel.send(embed=embed)
