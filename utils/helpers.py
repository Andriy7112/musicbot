# coding=utf-8
from main import bot
from data.messages import msg_dict


# Function to send waiting message
async def send_message(chat_id, msg_str, lang='ru', args=None, markup=None, markdown=None):
    user_text = await user_msg(msg_str, lang, args)
    await bot.send_message(chat_id, user_text, reply_markup=markup, parse_mode=markdown, disable_web_page_preview=True)


# Function to send music
async def send_audio(chat_id, file_to_send, title=None, performer=None, duration=None, thumb=None):
    try:
        sent_audio = await bot.send_audio(chat_id, file_to_send, caption='@Evomuzsavebot', title=title,
                                          thumb=thumb, performer=performer, duration=duration)
        return sent_audio.audio.file_id

    except Exception as err:
        print(err, '[ERROR] in send_audio music file is more 20 or 50 MB')
        return False


async def edit_message(text, chat_id, message_id, lang, markup=None, args=None):
    msg_to_edit = await user_msg(text, lang, args)
    await bot.edit_message_text(text=msg_to_edit, chat_id=chat_id, message_id=message_id, reply_markup=markup,
                                disable_web_page_preview=True)


async def get_chat_member(channel_id, chat_id):
    user_following_info = await bot.get_chat_member(channel_id, chat_id)
    return user_following_info


# Get user language
async def user_msg(message_str, lang, args=None):
    if args is None:
        user_message = msg_dict[lang][message_str]
    else:
        if type(args) != tuple:
            user_message = msg_dict[lang][message_str].format(args)
        else:
            user_message = msg_dict[lang][message_str].format(*args)

    return user_message
