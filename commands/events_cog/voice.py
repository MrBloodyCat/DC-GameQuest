import disnake
from disnake.ext import commands
import aiohttp
import io
import logging
from datetime import datetime, timedelta
from BANNED_FILES.config import LOG_CHANNEL_ID, Embed_Color


class VoiceLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = LOG_CHANNEL_ID
        self.webhook_cache = {}
        self.bot_avatar: bytes = b""
        self.bot.loop.create_task(self.prepare())
        self.embed_color = disnake.Color(int(Embed_Color.lstrip("#"), 16))

    async def prepare(self):
        await self.bot.wait_until_ready()
        await self.cache_bot_avatar()

    async def cache_bot_avatar(self):
        url = self.bot.user.avatar.url if self.bot.user.avatar else self.bot.user.default_avatar.url
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    self.bot_avatar = await resp.read()
        except Exception as e:
            logging.error(f"Ошибка при загрузке аватарки бота: {e}")

    async def get_or_create_webhook(self, channel: disnake.TextChannel) -> disnake.Webhook:
        webhook_name = f"{self.bot.user.name}_Voice"
        if channel.id in self.webhook_cache:
            return self.webhook_cache[channel.id]

        try:
            webhooks = await channel.webhooks()
            for wh in webhooks:
                if wh.name == webhook_name:
                    self.webhook_cache[channel.id] = wh
                    return wh

            webhook = await channel.create_webhook(name=webhook_name, avatar=self.bot_avatar)
            self.webhook_cache[channel.id] = webhook
            return webhook
        except disnake.Forbidden:
            logging.error(f"Нет прав создавать вебхуки в канале {channel.id}")
        except Exception as e:
            logging.error(f"Ошибка при получении или создании вебхука: {e}")

        return None

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        embed = disnake.Embed(color=self.embed_color)

        # Время по МСК
        moscow_time = (datetime.utcnow() + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')

        user_mention = f"<@{member.id}>"

        def channel_mention(ch):
            return f"<#{ch.id}>" if ch else "—"

        if not before.channel and after.channel:
            embed.title = "<:callcalling:1386045379765735465> Подключение к оперативной сети"
            embed.description = (
                f"Лейтенант {user_mention} десантировался в сектор. Оружие заряжено, юмор — тоже.\n\n"
                f"<:channel:1386045423348613270> **Сектор:** {channel_mention(after.channel)}\n"
                f"<:calendar:1386045347628974115> **Время подключения:** {moscow_time} по МСК\n\n"
            )
        elif before.channel and not after.channel:
            embed.title = "<:callslash:1386045391400599713> Исчез в радиопомехах"
            embed.description = (
                f"Лейтенант {user_mention} вышел из радиуса действия. Возможно, перешёл на другую частоту.\n\n"
                f"<:channel:1386045423348613270> **Сектор:** {channel_mention(before.channel)}\n"
                f"<:calendar:1386045347628974115> **Время отключения:** {moscow_time} по МСК\n\n"
            )
        elif before.channel != after.channel:
            embed.title = "<:calladd:1386045364586680501> Срочная эвакуация в другой войс"
            embed.description = (
                f"Лейтенант {user_mention} рванул в другой сектор, как будто за ним гнался ПВО.\n\n"
                f"<:channel:1386045423348613270> **Старый сектор:** {channel_mention(before.channel)}\n"
                f"<:channeladd:1386045408115163287> **Новый сектор:** {channel_mention(after.channel)}\n"
                f"<:calendar:1386045347628974115> **Время переключения:** {moscow_time} по МСК\n\n"
            )
        else:
            return  # Нет изменений

        await self.send_voice_log(member.guild, embed)

    async def send_voice_log(self, guild: disnake.Guild, embed: disnake.Embed):
        channel = guild.get_channel(self.log_channel_id)
        if not isinstance(channel, disnake.TextChannel):
            logging.error("Канал для логов не найден или не является текстовым")
            return

        if not self.bot_avatar:
            await self.cache_bot_avatar()

        webhook = await self.get_or_create_webhook(channel)
        if webhook is None:
            logging.error("Вебхук не получен, лог не отправлен")
            return

        try:
            await webhook.send(
                embed=embed,
                username=f"{self.bot.user.name}_Voice",
                allowed_mentions=disnake.AllowedMentions(users=True)  # разрешаем упоминания
            )
        except disnake.Forbidden:
            logging.error("Недостаточно прав для отправки сообщения через вебхук")
        except Exception as e:
            logging.error(f"Ошибка при отправке лога через вебхук: {e}")
