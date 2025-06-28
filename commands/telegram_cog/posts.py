import os
import asyncio
import disnake
from disnake.ext import commands
from telethon import TelegramClient, events, types
from telethon.tl.types import (MessageEntityBold, MessageEntityItalic, MessageEntityTextUrl, MessageEntityUrl, MessageEntityCode, MessageEntityPre, MessageEntityUnderline, MessageEntityStrike)
from BANNED_FILES.config import (api_id, api_hash, telegram_bot, TELEGRAM_ID, TELEGRAM_DISCORD_CHANNEL_ID, Download_Temp)

telegram_client = TelegramClient("telegram_session", api_id, api_hash)

def format_telegram_message(message_text, entities):
    if not entities or not message_text:
        return message_text or ""

    result = message_text
    inserts = []

    for entity in entities:
        start = entity.offset
        end = entity.offset + entity.length

        if isinstance(entity, MessageEntityBold):
            inserts.append((start, "**"))
            inserts.append((end, "**"))
        elif isinstance(entity, MessageEntityItalic):
            inserts.append((start, "*"))
            inserts.append((end, "*"))
        elif isinstance(entity, MessageEntityUnderline):
            inserts.append((start, "__"))
            inserts.append((end, "__"))
        elif isinstance(entity, MessageEntityStrike):
            inserts.append((start, "~~"))
            inserts.append((end, "~~"))
        elif isinstance(entity, MessageEntityCode):
            inserts.append((start, "`"))
            inserts.append((end, "`"))
        elif isinstance(entity, MessageEntityPre):
            inserts.append((start, "```"))
            inserts.append((end, "```"))
        elif isinstance(entity, MessageEntityTextUrl):
            text_part = result[start:end]
            inserts.append((start, f"[{text_part}]("))
            inserts.append((end, f"){entity.url}"))
        elif isinstance(entity, MessageEntityUrl):
            continue

    inserts.sort(reverse=True)
    for pos, mark in inserts:
        result = result[:pos] + mark + result[pos:]

    return result

class TelegramBridge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_map = {}
        self.grouped_media = {}
        self.grouped_tasks = {}
        self.bot.loop.create_task(self.init_telegram())

    async def init_telegram(self):
        await self.bot.wait_until_ready()
        try:
            await telegram_client.start(bot_token=telegram_bot)
            telegram_client.add_event_handler(self.handle_new_message, events.NewMessage(chats=TELEGRAM_ID))
            telegram_client.add_event_handler(self.handle_edit, events.MessageEdited(chats=TELEGRAM_ID))
            telegram_client.add_event_handler(self.handle_delete, events.MessageDeleted(chats=TELEGRAM_ID))
            print("Telegram client started successfully!")
            asyncio.create_task(telegram_client.run_until_disconnected())
        except Exception as e:
            print(f"Telegram client start error: {e}")

    async def handle_new_message(self, event):
        grouped_id = getattr(event.message, "grouped_id", None)

        if grouped_id:
            if grouped_id not in self.grouped_media:
                self.grouped_media[grouped_id] = []
            self.grouped_media[grouped_id].append(event)

            if grouped_id not in self.grouped_tasks:
                self.grouped_tasks[grouped_id] = asyncio.create_task(self.finalize_album(grouped_id))
        else:
            await self.send_to_discord([event])

    async def finalize_album(self, grouped_id):
        await asyncio.sleep(2.5)
        events = self.grouped_media.get(grouped_id, [])
        if events:
            await self.send_to_discord(events)
        self.grouped_media.pop(grouped_id, None)
        self.grouped_tasks.pop(grouped_id, None)

    async def send_to_discord(self, events):
        content = ""
        files = []
        os.makedirs(Download_Temp, exist_ok=True)

        for event in events:
            try:
                if not content and event.message.message:
                    content = format_telegram_message(
                        event.message.message,
                        event.message.entities
                    )[:2000]

                if event.message.media:
                    file_path = await self.download_media(event.message)
                    if file_path:
                        files.append(disnake.File(file_path))
            except Exception as e:
                print(f"Ошибка обработки медиа: {e}")

        channel = self.bot.get_channel(TELEGRAM_DISCORD_CHANNEL_ID)
        if not channel:
            print("Discord канал не найден")
            return

        try:
            discord_msg = await channel.send(
                content=content or None,
                files=files[:10] or None
            )
            self.message_map[events[0].message.id] = discord_msg.id
        except Exception as e:
            print(f"Ошибка отправки в Discord: {e}")
        finally:
            for f in files:
                try:
                    os.remove(f.fp.name)
                except Exception as e:
                    print(f"Ошибка удаления файла {f.fp.name}: {e}")

    async def download_media(self, message):
        try:
            ext = ".jpg" if isinstance(message.media, types.MessageMediaPhoto) else ""
            return await telegram_client.download_media(
                message,
                file=os.path.join(Download_Temp, f"media_{message.id}{ext}")
            )
        except Exception as e:
            print(f"Ошибка загрузки медиа: {e}")
            return None

    async def handle_edit(self, event):
        discord_id = self.message_map.get(event.message.id)
        if not discord_id:
            return

        channel = self.bot.get_channel(TELEGRAM_DISCORD_CHANNEL_ID)
        if not channel:
            return

        try:
            content = format_telegram_message(
                event.message.message,
                event.message.entities
            )[:2000]
            discord_msg = await channel.fetch_message(discord_id)
            await discord_msg.edit(content=content)
        except Exception as e:
            print(f"Ошибка редактирования в Discord: {e}")

    async def handle_delete(self, event):
        channel = self.bot.get_channel(TELEGRAM_DISCORD_CHANNEL_ID)
        if not channel:
            return

        for msg_id in event.deleted_ids:
            discord_id = self.message_map.get(msg_id)
            if not discord_id:
                continue
            try:
                msg = await channel.fetch_message(discord_id)
                await msg.delete()
                del self.message_map[msg_id]
            except Exception as e:
                print(f"Ошибка удаления сообщения в Discord: {e}")
