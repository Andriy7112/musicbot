from aiogram.types import Message

from utils.helpers import send_message
from main import dp, users_db


# Ответ на команды по музыке
@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    users_db.set(message.chat.id, 'ru')
    await send_message(message.chat.id, 'start', markdown='markdown')

