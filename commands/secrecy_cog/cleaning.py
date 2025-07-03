import disnake
from disnake.ext import commands
import asyncio
from datetime import datetime, timedelta
from BANNED_FILES.config import Embed_Color, Message_Cleaning, ALLOWED_USER_IDS

class CleanCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed_color = disnake.Color(int(Embed_Color.lstrip("#"), 16))

    @commands.command(name="зачистка", help="Зачистка канала связи")
    @commands.has_permissions(manage_messages=True)
    async def purge_channel(self, ctx: commands.Context):
        # Проверка разрешения по списку
        if ctx.author.id not in ALLOWED_USER_IDS:
            return  # Игнорируем команду если пользователя нет в списке

        try:
            await ctx.channel.purge(limit=Message_Cleaning)

            moscow_time = (datetime.utcnow() + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")

            embed = disnake.Embed(
                title="<:infocircle:1390374048650760324>  Доклад о выполненной очистке канала связи",
                description=(
                    f"```Согласно оперативному распоряжению командования, проведена полная нейтрализация информационного шума. Передача данных восстановлена.```\n"
                    f"<:calendar:1386045347628974115> **Время доклада:** {moscow_time} по МСК"
                ),
                color=self.embed_color
            )

            msg = await ctx.send(embed=embed)
            await asyncio.sleep(10)
            await msg.delete()

        except Exception as e:
            await ctx.send(f"⚠️ Ошибка при выполнении операции: {e}")
