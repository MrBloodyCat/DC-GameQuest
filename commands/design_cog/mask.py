import os
import random
import disnake
from disnake.ext import commands
from disnake.ui import View, Button
from BANNED_FILES.config import Embed_Color, Avatar_Folder


class ProAvatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed_color = disnake.Color(int(Embed_Color.lstrip("#"), 16))
        self.avatars = [f for f in os.listdir(Avatar_Folder)
                        if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]

    @commands.slash_command(name="камуфляж", description="Панель маскировочных протоколов")
    async def avatar_viewer(self, inter: disnake.AppCmdInter):
        if not self.avatars:
            await inter.response.send_message("❌ В арсенале нет ни одного камуфляжа.")
            return

        current_index = 0
        file_path = os.path.join(Avatar_Folder, self.avatars[current_index])
        file = disnake.File(file_path, filename="GameQuest_Camouflage.png")

        username = inter.author.display_name

        embed = disnake.Embed(
            title=f"<:userhexagon:1391013148592443463> Панель голограм {inter.guild.name}",
            description=(
                f"> Приступай, лейтенант **{username}** к подготовке. **Выбери** подходящий камуфляж для предстоящей операции."
            ),
            color=self.embed_color
        )
        embed.set_image(url="attachment://GameQuest_Camouflage.png")
        embed.set_footer(text=f"{current_index + 1} / {len(self.avatars)} — голограм от команди {inter.guild.name}")

        view = PromoAvatar(self.avatars, current_index, self.embed_color, inter.guild.name, username)
        await inter.response.send_message(embed=embed, file=file, view=view)


class PromoAvatar(View):
    def __init__(self, avatars, current_index, embed_color, guild_name, username):
        super().__init__(timeout=180)
        self.avatars = avatars
        self.current_index = current_index
        self.embed_color = embed_color
        self.guild_name = guild_name
        self.username = username

        self.prev_button = Button(
            label="Назад",
            emoji="<:directleft:1391047142344491101>",
            style=disnake.ButtonStyle.success
        )
        self.random_button = Button(
            label="Случайная",
            emoji="<:radom:1391048248528994314>",
            style=disnake.ButtonStyle.primary
        )
        self.next_button = Button(
            label="Вперёд",
            emoji="<:directright:1391047155157831770>",
            style=disnake.ButtonStyle.success
        )

        self.prev_button.callback = self.go_back
        self.random_button.callback = self.go_random
        self.next_button.callback = self.go_forward

        self.add_item(self.prev_button)
        self.add_item(self.random_button)
        self.add_item(self.next_button)

    async def go_back(self, interaction: disnake.MessageInteraction):
        self.current_index = (self.current_index - 1) % len(self.avatars)
        await self.update_embed(interaction)

    async def go_forward(self, interaction: disnake.MessageInteraction):
        self.current_index = (self.current_index + 1) % len(self.avatars)
        await self.update_embed(interaction)

    async def go_random(self, interaction: disnake.MessageInteraction):
        if len(self.avatars) > 1:
            prev_index = self.current_index
            while self.current_index == prev_index:
                self.current_index = random.randint(0, len(self.avatars) - 1)
        await self.update_embed(interaction)

    async def update_embed(self, interaction: disnake.MessageInteraction):
        file_path = os.path.join(Avatar_Folder, self.avatars[self.current_index])
        file = disnake.File(file_path, filename="GameQuest_Camouflage.png")

        embed = disnake.Embed(
            title=f"<:userhexagon:1391013148592443463> Панель голограм {self.guild_name}",
            description=(
                f"> Приступай, лейтенант **{self.username}** к подготовке. **Выбери** подходящий камуфляж для предстоящей операции."
            ),
            color=self.embed_color
        )
        embed.set_image(url="attachment://GameQuest_Camouflage.png")
        embed.set_footer(text=f"{self.current_index + 1} / {len(self.avatars)} — голограм от команди {self.guild_name}")

        await interaction.response.edit_message(embed=embed, file=file, view=self)
