import disnake
from disnake.ext import commands
import os
from BANNED_FILES.config import Embed_Color, Barrier_Gif

class LanguageInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed_color = disnake.Color(int(Embed_Color.lstrip("#"), 16))

    @commands.slash_command(name="язык", description="Серверный регламент языков")
    async def language_status(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()

        embed = disnake.Embed(
            title="<:translate:1390369466260525136> Коммуникационный модуль базы",
            description="> Единые стандарты коммуникации, утверждённые оперативным штабом, регулируют передачу данных и обязательны для исполнения всеми участниками.",
            color=self.embed_color
        )

        embed.add_field(
            name="<:textalignleft:1390369452675043388> **Языки лейтенантов в операциях:**",
            value="Русский — основной язык стратегической связи\n"
                  "Украинский — используется в региональных задачах\n"
                  "Английский — применяется при международных контактах",
            inline=False
        )

        embed.add_field(
            name="<:textalignleft:1390369452675043388> **Командная связь с сержантом:**",
            value="Ведётся исключительно на русском языке, другие варианты не поддерживаются системой",
            inline=False
        )

        embed.set_footer(text="Благодарим за проявленный интерес к нашему спецпроекту!")

        gif_path = Barrier_Gif
        if not os.path.exists(gif_path):
            await inter.edit_original_response("Анимация не обнаружена. Проверь путь к гифке.")
            return

        file = disnake.File(gif_path, filename="language.gif")
        embed.set_image(url="attachment://language.gif")

        await inter.edit_original_response(embed=embed, file=file)
