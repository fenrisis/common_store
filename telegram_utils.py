from aiogram import Bot
import asyncio

TOKEN = "*****"
bot = Bot(token=TOKEN)

async def send_telegram_message(username: str, message: str):
    try:
        # Добавляем @ перед username, если его там нет
        if not username.startswith("@"):
            username = "@" + username

        user = await bot.get_chat(username)
        await bot.send_message(chat_id=user.id, text=message)
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")