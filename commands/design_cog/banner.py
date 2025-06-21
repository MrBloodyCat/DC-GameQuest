import disnake
from disnake.ext import commands


class BannerView(disnake.ui.View):
    def __init__(self, user: disnake.User):
        super().__init__(timeout=None)
        self.user = user

    @disnake.ui.button(label="Обновить баннер", style=disnake.ButtonStyle.blurple)
    async def refresh_banner_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        banner_url = self.user.banner.url if self.user.banner else None

        if banner_url:
            embed = disnake.Embed(
                title=f"Баннер — {self.user.display_name}",
                description="Это пользовательский баннер профиля.",
                color=disnake.Color.blurple()
            )
            embed.set_image(url=banner_url)
        else:
            embed = disnake.Embed(
                title=f"Баннер — {self.user.display_name}",
                description="У пользователя нет баннера профиля.",
                color=disnake.Color.red()
            )

        await interaction.response.edit_message(embed=embed, view=self)


class BannerCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="banner", description="Показать баннер пользователя.")
    async def banner(self, inter: disnake.AppCmdInter, пользователь: disnake.User = None):
        user = пользователь or inter.author
        banner_url = user.banner.url if user.banner else None

        if banner_url:
            embed = disnake.Embed(
                title=f"Баннер — {user.display_name}",
                description="Это пользовательский баннер профиля.",
                color=disnake.Color.blurple()
            )
            embed.set_image(url=banner_url)
        else:
            embed = disnake.Embed(
                title=f"Баннер — {user.display_name}",
                description="У пользователя нет баннера профиля.",
                color=disnake.Color.red()
            )

        view = BannerView(user)
        await inter.response.send_message(embed=embed, view=view)


def setup(bot: commands.Bot):
    bot.add_cog(BannerCommands(bot))

