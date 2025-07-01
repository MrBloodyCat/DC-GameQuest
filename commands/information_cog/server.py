import disnake
from disnake.ext import commands
from datetime import datetime
import os
from BANNED_FILES.config import Embed_Color, Assembly_Gif

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed_color = disnake.Color(int(Embed_Color.lstrip("#"), 16))

    @commands.slash_command(name="сервер", description="Сканирование серверной инфраструктуры")
    async def serverinfo(self, inter: disnake.AppCmdInter):
        await inter.response.defer() 

        guild = inter.guild
        if not guild:
            await inter.edit_original_response("🔒 Команда доступна только внутри укреплённого объекта (сервера).")
            return

        commander = guild.owner.mention
        created = guild.created_at.strftime("%d.%m.%Y")
        server_id = guild.id
        description = guild.description or "📡 Назначение и цели объекта: засекречены."

        total_members = guild.member_count
        online_members = sum(m.status != disnake.Status.offline for m in guild.members)
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        roles = len(guild.roles)
        categories = len(guild.categories)
        boost_level = guild.premium_tier
        boost_count = guild.premium_subscription_count

        embed = disnake.Embed(
            title=f"<:courthouse:1388889492865155153> Картирование инфраструктуры {guild.name}",
            description=(
                "> Оперативный отчёт о боеспособности подразделения, стабильности каналов связи и состоянии оборонительных позиций.\n\n"
                f"<:usersquar:1388889541645172957> **Адмирал базы:** {commander}\n"
                f"<:calendar2:1388889677297352837> **Дата основания:** `{created}`\n"
                f"<:driver:1388889638256644189> **Индикатор базы:** `{server_id}`\n\n"
                f"<:textalign:1388889563640103032> **Описание базы:**\n```{description}```\n"
                f"<:people:1388889582354960608> **Личный состав:** `Всего: {total_members}` | `Активны: {online_members}`\n"
                f"<:char:1388889657906827395> **Каналы связи:** `Текстовых: {text_channels}` | `Голосовых: {voice_channels}`\n"
                f"<:graph:1388889597882269717> **Структура базы:** `Ролей: {roles}` | `Категорий: {categories}`\n"
                f"<:flash:1388889612818186250> **Поддержка базы:** `Уровень: {boost_level}` | `Бустов: {boost_count}`"
            ),
            color=self.embed_color
        )

        embed.set_footer(text="Благодарим за проявленный интерес к нашему спецпроекту!")

        gif_path = Assembly_Gif
        if not os.path.exists(gif_path):
            await inter.edit_original_response("❌ Анимация не обнаружена. Проверь путь к гифке.")
            return

        file = disnake.File(gif_path, filename="military.gif")
        embed.set_image(url="attachment://military.gif")

        await inter.edit_original_response(embed=embed, file=file)
