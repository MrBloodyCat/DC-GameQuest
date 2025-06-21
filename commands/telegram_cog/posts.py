import os
import asyncio
import disnake
from disnake.ext import commands
from telethon import TelegramClient, events
from BANNED_FILES.config import api_id, api_hash, telegram_bot, TELEGRAM_ID, TELEGRAM_DISCORD_CHANNEL_ID, Download_Temp

telegram_client = TelegramClient("telegram_session", api_id, api_hash)

class TelegramBridge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_map = {}  # {telegram_msg_id: discord_msg_id}
        self.bot.loop.create_task(self.init_telegram())

    async def init_telegram(self):
        await self.bot.wait_until_ready()
        try:
            await telegram_client.start(bot_token=telegram_bot)
            telegram_client.add_event_handler(self.forward_to_discord, events.NewMessage(chats=TELEGRAM_ID))
            telegram_client.add_event_handler(self.edit_to_discord, events.MessageEdited(chats=TELEGRAM_ID))
            telegram_client.add_event_handler(self.delete_to_discord, events.MessageDeleted(chats=TELEGRAM_ID))
            print("Telegram client started successfully!")
            asyncio.create_task(telegram_client.run_until_disconnected())
        except:
            pass

    async def forward_to_discord(self, event):
        content = event.text or ""
        files = []

        if event.media:
            try:
                os.makedirs(Download_Temp, exist_ok=True)
                filename = f"{Download_Temp}/telegram_{event.id}"
                path = await telegram_client.download_media(event.media, file=filename)
                if path:
                    files.append(disnake.File(path))
            except:
                pass

        channel = self.bot.get_channel(TELEGRAM_DISCORD_CHANNEL_ID)
        if not channel:
            return

        try:
            discord_msg = await channel.send(content if content else "Media message:", files=files)
            self.message_map[event.id] = discord_msg.id

            # Запускаем таймер на 3 минуты, чтобы удалить ID из message_map
            self.bot.loop.create_task(self.expire_message(event.id, delay=180))
        except:
            pass

        for f in files:
            try:
                os.remove(f.fp.name)
            except:
                pass

    async def edit_to_discord(self, event):
        discord_id = self.message_map.get(event.id)
        if not discord_id:
            return

        channel = self.bot.get_channel(TELEGRAM_DISCORD_CHANNEL_ID)
        if not channel:
            return

        try:
            dm = await channel.fetch_message(discord_id)
            await dm.edit(content=event.text or "")
        except:
            pass

    async def delete_to_discord(self, event):
        channel = self.bot.get_channel(TELEGRAM_DISCORD_CHANNEL_ID)
        if not channel:
            return

        for tid in event.deleted_ids:
            did = self.message_map.get(tid)
            if not did:
                continue
            try:
                msg = await channel.fetch_message(did)
                await msg.delete()
                del self.message_map[tid]
            except:
                pass

    async def expire_message(self, telegram_msg_id, delay=180):
        await asyncio.sleep(delay)
        self.message_map.pop(telegram_msg_id, None)
