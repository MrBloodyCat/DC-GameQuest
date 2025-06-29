import disnake
from disnake.ext import commands
from BANNED_FILES.config import CHAT_CHANNEL_ID, Embed_Color, Social_Subscription, Social_Donate, Social_Image

class AutoPromo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = CHAT_CHANNEL_ID

        self.message_threshold_sub = Social_Subscription
        self.message_threshold_donate = Social_Donate

        self.counter_sub = 0
        self.counter_donate = 0

        self.embed_color = disnake.Color(int(Embed_Color.lstrip("#"), 16))

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.channel.id != self.channel_id or message.author.bot:
            return

        self.counter_sub += 1
        self.counter_donate += 1

        image_path = Social_Image
        file = disnake.File(image_path, filename="banner.jpg")
        image_url = "attachment://banner.jpg"

        if self.counter_sub >= self.message_threshold_sub:
            embed = disnake.Embed(
                title="<:aiusers:1388576262355943434> Оперативная сводка по социальным платформам",
                description=(
                    "Товарищи лейтенанты! Команда **Game Quest** напоминает о необходимости **контроля** всех секторов информационного фронта!\n\n"
                    "<:youtube:1385657711110393856> **YouTube:** https://www.youtube.com/@GameQuest_news\n"
                    "<:tg:1388590213567221801> **Telegram:** https://t.me/GameQuest_news\n"
                    "<:dc:1388590201349079050> **Discord:** https://discord.gg/GJUuPRbN5a\n"
                    "<:vk:1385657735793742097> **ВКонтактe:** https://t.me/GameQuest_news"
                ),
                color=self.embed_color
            )
            embed.set_image(url=image_url)
            embed.set_footer(text="Благодарим за проявленный интерес к нашему спецпроекту!")

            await message.channel.send(embed=embed, file=file)
            self.counter_sub = 0

        if self.counter_donate >= self.message_threshold_donate:
            embed = disnake.Embed(
                title="<:userai:1388576282538807487> Мониторинг добровольных пожертвований",
                description=(
                    "Товарищи лейтенанты! Команда **Game Quest** напоминает что ваш вклад в операцию по развитию **укрепляет** наши позиции на информационном фронте!\n\n"
                    "<:wallet:1388579605379682438> **Patreon:**\n https://www.patreon.com/andremuhamad\n"
                    "<:wallet:1388579605379682438> **DonationAlerts:**\n https://www.donationalerts.com/r/andremuhamad"
                ),
                color=self.embed_color
            )
            embed.set_image(url=image_url)
            embed.set_footer(text="Благодарим за проявленный интерес к нашему спецпроекту!")

            await message.channel.send(embed=embed, file=file)
            self.counter_donate = 0
