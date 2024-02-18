import traceback
from aiogram import Bot
import asyncio

TOKEN = "*******"
bot = Bot(token=TOKEN)


async def send_telegram_message(chat_id: int, message: str):
    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")