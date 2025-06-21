import disnake
from disnake.ext import commands
from datetime import datetime

class ServerInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="serverinfo", description="📊 Получить информацию о текущем сервере.")
    @commands.cooldown(rate=1, per=10)
    async def serverinfo(self, inter: disnake.AppCmdInter):
        guild = inter.guild

        if not guild:
            await inter.response.send_message("Эта команда доступна только на сервере.", ephemeral=True)
            return

        owner = guild.owner
        creation_date = guild.created_at.strftime('%d.%m.%Y')
        description = guild.description or "Нет описания."

        role_count = len(guild.roles)
        channel_count = len(guild.channels)
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        online_members = sum(member.status != disnake.Status.offline for member in guild.members)
        boost_level = guild.premium_tier
        boost_count = guild.premium_subscription_count

        embed = disnake.Embed(
            title=f"📊 Сервер: {guild.name}",
            color=0x2b2d31,
            timestamp=datetime.now()
        )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        embed.add_field(name="👑 Владелец", value=owner.mention, inline=True)
        embed.add_field(name="📅 Создан", value=f"`{creation_date}`", inline=True)
        embed.add_field(name="📝 Описание", value=f"```{description}```", inline=False)
        embed.add_field(name="👥 Участники", value=f"Всего: `{guild.member_count}`\nОнлайн: `{online_members}`", inline=True)
        embed.add_field(name="📊 Роли и каналы", value=f"Ролей: `{role_count}`\nКаналов: `{channel_count}`", inline=True)
        embed.add_field(name="🔈 Каналы", value=f"Текстовые: `{text_channels}`\nГолосовые: `{voice_channels}`", inline=True)

        if boost_level > 0:
            embed.add_field(name="✨ Бусты", value=f"Уровень: `{boost_level}`\nКоличество: `{boost_count}`", inline=True)

        embed.set_footer(text=f"ID сервера: {guild.id}")

        await inter.response.send_message(embed=embed)
