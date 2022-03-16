from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

admin_buttons = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
admin_button_1 = KeyboardButton('Рассылка рекламы')
admin_button_2 = KeyboardButton('Бекап базы')
admin_button_3 = KeyboardButton('Статистика бота')
admin_buttons.add(*[admin_button_1, admin_button_2, admin_button_3])


admin_lang_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
russian_lang = KeyboardButton('Русский')
english_lang = KeyboardButton('Английский')
uzbek_lang = KeyboardButton('Узбекский')
reject_button = KeyboardButton('Отменить')
admin_lang_markup.add(*[russian_lang, english_lang, uzbek_lang, reject_button])


admin_state_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
skip_state = KeyboardButton('Пропустить')
reject_button = KeyboardButton('Отменить')
admin_state_markup.add(*[skip_state, reject_button])


admin_reject_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
reject_button = KeyboardButton('Отменить')
admin_reject_markup.add(reject_button)

admin_sure_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
send_button = KeyboardButton('Начать')
reject_button = KeyboardButton('Отменить')
admin_sure_markup.add(*[send_button, reject_button])


follow_markup = InlineKeyboardMarkup(row_width=1)
follow_check_button = InlineKeyboardButton(text='Подписался󠁧󠁢󠁥󠁮󠁧󠁿󠁢󠁥󠁮󠁧󠁿󠁢󠁥󠁮󠁧󠁿', callback_data='check')
follow_button = InlineKeyboardButton(text='Подписаться на канал󠁧󠁢󠁥󠁮󠁧󠁿󠁢󠁥󠁮󠁧󠁿󠁢󠁥󠁮󠁧󠁿', url='https://t.me/joinchat/_CgxauJGxtpmNjFi')
follow_markup.add(*[follow_button, follow_check_button])




