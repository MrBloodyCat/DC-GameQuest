import disnake
import os
from dotenv import load_dotenv
from disnake.ext import commands
from BANNED_FILES.config import discord_bot

# Загрузка переменных окружения
load_dotenv()

# Настройка intents
intents = disnake.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
intents.presences = True
intents.voice_states = True
intents.guilds = True

# Инициализация бота
bot = commands.Bot(command_prefix="!", intents=intents)

# Событие при запуске
@bot.event
async def on_ready():
    print(f"Bot {bot.user} is up and running!")

# Загружаем коги
bot.load_extension("commands.status_cog") # Папка статус

bot.load_extension("commands.speaker_cog") # Папка спикер

bot.load_extension("commands.design_cog") # Папка с дизайном профилей дискорда

bot.load_extension("commands.telegram_cog") # Папка с подключения постинга из Telegram

bot.load_extension("commands.messages_cog") # Папка с сообщениями от бота

bot.load_extension("commands.ember_cog") # Папка с ембитам для отправки

bot.load_extension("commands.events_cog") # Папка с событиями на сервере и боте

bot.load_extension("commands.reaction_cog") # Папка с рекциями на сообщения

bot.load_extension("commands.moderation_cog") # Папка с модерацией

# Запуск
if __name__ == "__main__":
    bot.run(discord_bot)
