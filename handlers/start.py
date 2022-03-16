from aiogram.types import Message

from keyboards.buttons import follow_markup
from utils.help_functions import check_channel_following
from utils.helpers import send_message
from main import dp, users_db


# Ответ на команды по музыке
@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    chat_id = message.chat.id
    users_db.set(message.chat.id, 'ru')

    is_following = await check_channel_following(chat_id)
    if not is_following:
        await send_message(chat_id, 'channel', markup=follow_markup, markdown='markdown')
        return
    else:
        await send_message(chat_id, 'start', markdown='markdown')

