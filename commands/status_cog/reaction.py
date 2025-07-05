import disnake
from disnake.ext import commands
import datetime
from BANNED_FILES.config import Embed_Color

class MentionResponse(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.embed_color = disnake.Color(int(Embed_Color.lstrip("#"), 16))

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot:
            return

        if self.bot.user.mentioned_in(message):
            latency = round(self.bot.latency * 1000)

            # Подсчёт аптайма
            now = datetime.datetime.utcnow()
            uptime = now - getattr(self.bot, "start_time", now)
            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            uptime_str = f"{days}д {hours}ч {minutes}м {seconds}с"

            embed = disnake.Embed(
                title=f"<:airdrop:1390972469073936414> Штаб зафиксировал ваше имя — {message.author.display_name}!",
                description=(
                    "Здравия желаю! Я здесь и всегда готов **помочь** и внести вклад в проект **Game Quest**.\n\n"
                    f">>> Мой военный пинг: `{latency} мс`\n"
                    f"Время несения службы: `{uptime_str}`\n"
                    "Мои создатели: <@768782555171782667> и <@787093771115692062>\n"
                    "Website Muhameda: [muhamedlabs.pro](https://muhamedlabs.pro)"
                ),
                color=self.embed_color
            )
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(text="Благодарим за проявленный интерес к нашему спецпроекту!")

            await message.channel.send(embed=embed)
