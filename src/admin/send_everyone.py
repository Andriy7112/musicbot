# coding=utf-8
from time import time
import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from main import users_db, dp, bot, AdminSendEveryOne, ADMIN_ID, AD_CHANNEL_ID
from keyboards.buttons import admin_reject_markup, admin_sure_markup, admin_buttons


# Ask admin to send gif or photo
async def send_everyone_func():
    await bot.send_message(ADMIN_ID, 'Перешлите пост для рассылки.', reply_markup=admin_reject_markup)
    await AdminSendEveryOne.ask_post.set()


# Check admin sent message or file
@dp.message_handler(state=AdminSendEveryOne.ask_post, content_types=['photo', 'text', 'animation'])
async def admin_post_type(message: Message, state: FSMContext):
    if message.text == 'Отменить':
        await reject_message(state)
        return

    await state.update_data(buttons=message.reply_markup)
    await state.update_data(message_id=message.forward_from_message_id)

    await bot.copy_message(ADMIN_ID, AD_CHANNEL_ID, message.forward_from_message_id, reply_markup=message.reply_markup)
    await bot.send_message(ADMIN_ID, 'Ваш пост будет выглядеть так, начать рассылку?', reply_markup=admin_sure_markup)

    await AdminSendEveryOne.ask_send.set()


# Ask, if the admin sure to start sending advertisement
@dp.message_handler(state=AdminSendEveryOne.ask_send)
async def admin_ask_send(message: Message, state: FSMContext):
    if message.text == 'Отменить':
        await reject_message(state)
        return

    if message.text == 'Начать':
        await bot.send_message(ADMIN_ID, 'Рассылка началась!', reply_markup=admin_buttons)
        await send_post(state)
        return

    await bot.send_message(ADMIN_ID, 'Начать рассылку или отменить?', reply_markup=admin_sure_markup)
    await AdminSendEveryOne.ask_send.set()


# Function for sending advertisement
async def send_post(state):
    data = await state.get_data()
    message_id = data.get('message_id')
    buttons = data.get('buttons')

    await state.finish()

    list_users_id = users_db.keys()

    delete = 0
    success = 0

    sent_message = await bot.send_message(ADMIN_ID, '{0:,} пользователей получили рассылку'.format(success))

    start_time = int(time())
    for i, user_id in enumerate(list_users_id):
        if success % 5000 == 0 and success != 0:
            await bot.delete_message(ADMIN_ID, sent_message.message_id)
            sent_message = await bot.send_message(ADMIN_ID, '{0:,} пользователей получили рассылку'.format(success))

        try:
            await bot.copy_message(int(user_id), AD_CHANNEL_ID, message_id, disable_notification=True, reply_markup=buttons)
            success += 1
        except Exception as err:
            print(err)
            users_db.set(user_id, 'None')
            delete += 1

    taken_time = int(time()) - start_time
    correct_time = str(datetime.timedelta(seconds=taken_time))

    admin_stat = "Рассылку получили: {0:,}\n" \
                 "Удалили: {1:,}\n" \
                 "Длительность рассылки: {2}".format(success, delete, correct_time)

    await bot.send_message(ADMIN_ID, admin_stat, reply_markup=admin_buttons)
    await bot.delete_message(ADMIN_ID, sent_message.message_id)


async def reject_message(state):
    await bot.send_message(ADMIN_ID, 'Вы отменили действия', reply_markup=admin_buttons)
    await state.finish()
