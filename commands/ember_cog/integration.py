import disnake
from disnake.ext import commands
from BANNED_FILES.config import Embed_Color, Video_Text, VIDEO_CHANNEL_ID  # добавляем ID канала

class IntegrationAnnouncer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed_color = disnake.Color(int(Embed_Color.lstrip("#"), 16))
        self.static_header = Video_Text  # Статичное верхнее сообщение

    @commands.slash_command(name="видео", description="Отправить интеграцию в youtube-дайджесты")
    async def видео(
        self,
        ctx: disnake.ApplicationCommandInteraction,
        превью: str,
        название: str,
        youtube: str,
        vkontakte: str
    ):
        """Отправляет embed с заголовком, изображением и ссылками на YouTube и ВКонтакте."""

        # Получение канала по ID
        канал = self.bot.get_channel(VIDEO_CHANNEL_ID)
        if not канал:
            await ctx.response.send_message("Канал не найден. Проверь VIDEO_CHANNEL_ID.", ephemeral=True)
            return

        # Создание Embed
        embed = disnake.Embed(
            title=f"{название}",
            color=self.embed_color
        )
        embed.set_image(url=превью)
        embed.add_field(name="<:youtube:1385657711110393856> YouTube:", value=youtube, inline=False)
        embed.add_field(name="<:vk:1385657735793742097> ВКонтакте:", value=vkontakte, inline=False)
        embed.set_footer(text="Благодарим за проявленный интерес к нашему спецпроекту!")

        # Отправка сообщения
        await канал.send(content=self.static_header, embed=embed)

        # Ответ пользователю
        await ctx.response.send_message(
            f"Интеграция успешно отправлена в {канал.mention}",
            ephemeral=True
        )