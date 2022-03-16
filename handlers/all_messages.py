from aiogram.types import Message

from keyboards.buttons import follow_markup
from main import dp
from utils.help_functions import check_channel_following
from utils.helpers import send_message
from utils.vk.vk_audio_message import vk_audio_message_main


@dp.message_handler()
@dp.throttled(rate=1)  # Prevent flooding
async def all_messages(message: Message):
    chat_id = message.chat.id
    user_message = message.text

    is_following = await check_channel_following(chat_id)
    if not is_following:
        await send_message(chat_id, 'channel', markup=follow_markup, markdown='markdown')
        return

    await vk_audio_message_main(chat_id, user_message, 'ru')
