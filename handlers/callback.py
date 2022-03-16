from aiogram.types import CallbackQuery

from main import dp
from utils.help_functions import check_channel_following
from utils.helpers import send_message
from utils.vk.vk_inline_call import vk_music_inline_call


# Ответ на нажатие кнопки
@dp.callback_query_handler(lambda call: True)
async def call_back_message(call: CallbackQuery):
    chat_id = call.message.chat.id
    call_message_id = call.message.message_id
    call_data = str(call.data)

    await call.answer()

    # Update user lang
    if call_data == 'check':
        is_following = await check_channel_following(chat_id)
        if is_following:
            try:
                await call.message.delete()
            except:
                pass
            await send_message(chat_id, 'start')
            await call.answer()
        else:
            await call.answer('Вы не подписались на канал!', show_alert=True)

        return

    if 'delete' in call_data:
        try:
            await call.message.delete()
        except:
            pass
        return

    else:
        split_data = str(call_data).split('!!!')
        if len(split_data) == 3:
            try:
                await call.message.delete()
            except:
                pass
            return

        try:
            await vk_music_inline_call(split_data, chat_id, call_message_id)
        except Exception as err:
            print(err)
