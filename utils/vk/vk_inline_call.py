import datetime
import json
import os

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from main import search_db, files_id, bot
from utils.help_functions import save_user_actions, download_vk_music
from utils.helpers import send_message, send_audio, edit_message, user_msg
from utils.vk.vk_website_audio_kiss import get_kiss_vk_music
from utils.vk.vk_website_audio_seven import get_music_seven


async def vk_music_inline_call(split_data, chat_id, message_id):
    user_lang = split_data[0]
    json_id = split_data[1]
    direction = split_data[2]
    music_list_number = int(split_data[3])

    # Get json audio by json id
    json_info = search_db.get(json_id)
    if json_info is None:
        await edit_message('audio-search-expired', chat_id, message_id, user_lang)
        return

    # Check, which button user pushed
    list_audio_dict = json.loads(json_info)['items']

    # Download audio by button number
    if direction == 'current':
        directory = await send_called_audio(list_audio_dict[music_list_number], chat_id, user_lang)
        if 'music' in directory:
            audio_dict = list_audio_dict[music_list_number]
            title = audio_dict['title']
            performer = audio_dict['artist']
            duration = audio_dict['duration']
            sent_audio = await bot.send_audio(chat_id, open(directory, 'rb'), caption='@Evomuzsavebot',
                                              title=title, performer=performer, duration=duration)
            audio_id = sent_audio.audio.file_id

            # Save audio id to database
            if audio_id:
                vk_audio_id = '{0}_{1}'.format(audio_dict['owner_id'], audio_dict['id'])
                files_id.set(vk_audio_id, audio_id)

            if os.path.exists(directory):
                os.remove(directory)

    # Switch to next and previous pages
    elif any(direction == x for x in ['prev', 'next']):
        if any(x == music_list_number for x in [0, len(list_audio_dict)]) and direction == 'next':
            return

        if music_list_number == -10 and direction == 'prev':
            return

        args, inline_markup = await get_audio_list_args(json_id, list_audio_dict, user_lang, music_list_number)
        await edit_message('audio-search-result', chat_id, message_id, user_lang, markup=inline_markup, args=args)

    else:
        # Download all page audios of search result
        music_count = len(list_audio_dict)
        for range_i in range(10):
            next_music_number = music_list_number + range_i
            if next_music_number + 1 == music_count:
                break

            await send_called_audio(list_audio_dict[next_music_number], chat_id, user_lang)


# Create inline buttons and list music result
async def get_audio_list_args(json_id, list_audio_dict, lang, start=0):
    inline_markup = InlineKeyboardMarkup(row_width=5)

    list_music_result = []
    list_inline_buttons = []
    audio_number = 0

    # Generate list results and buttons with numbers
    for i, audio_dict in enumerate(list_audio_dict):
        if i in range(start, start + 10):
            audio_number += 1
            title = audio_dict['title']
            performer = audio_dict['artist']
            duration_seconds = audio_dict['duration']

            duration_split = str(datetime.timedelta(seconds=duration_seconds)).split(':')

            music_result = f'{audio_number}. {title} - {performer} ⎮ {duration_split[1]}:{duration_split[2]}'
            music_replaced_result = music_result.replace('<', '')
            inline_button = InlineKeyboardButton(text=audio_number, callback_data=f'{lang}!!!{json_id}!!!current!!!{str(i)}')

            list_music_result.append(music_replaced_result)
            list_inline_buttons.append(inline_button)

        if i == start + 10:
            break

    # Calculate next and previous buttons
    if len(list_audio_dict) <= 10:
        prev_button_data = start - 10
        next_button_data = 0
        end = len(list_audio_dict)
    else:
        prev_button_data = start - 10
        next_button_data = start + 10

        if len(list_music_result) < 10:
            end = len(list_audio_dict)
            next_button_data = 0
        else:
            end = start + 10

    all_list_button_text = await user_msg('button-download-list', lang)
    prev_button = InlineKeyboardButton(text='⬅️', callback_data=f'{lang}!!!{json_id}!!!prev!!!{prev_button_data}')
    delete_button = InlineKeyboardButton(text='❌️', callback_data=f'{lang}!!!{json_id}!!!delete')
    next_button = InlineKeyboardButton(text='➡️', callback_data=f'{lang}!!!{json_id}!!!next!!!{next_button_data}')
    all_list_button = InlineKeyboardButton(text=all_list_button_text, callback_data=f'{lang}!!!{json_id}!!!page!!!{start}')

    # Add next, previous, all and delete buttons
    inline_markup.add(*list_inline_buttons)
    inline_markup.add(all_list_button)
    inline_markup.add(*[prev_button, delete_button, next_button])

    args = start + 1, end, len(list_audio_dict), '\n'.join(list_music_result)

    return args, inline_markup


# Function to send called audio
async def send_called_audio(audio_dict, chat_id, lang):
    # Get all needed data for audio
    title = audio_dict['title']
    performer = audio_dict['artist']
    audio_url = audio_dict['url']
    duration = audio_dict['duration']

    vk_audio_id = '{0}_{1}'.format(audio_dict['owner_id'], audio_dict['id'])
    await save_user_actions()

    # If music is in database, send by audio id
    music_file_id = files_id.get(vk_audio_id)

    if music_file_id is not None:
        await send_audio(chat_id, str(music_file_id, 'utf-8'))
        return

    # if no audio url, get audio url from kiss vk or music seven
    if audio_url == '':
        audio_url = await get_kiss_vk_music(title, performer, vk_audio_id)
        print('11111 (audio_url) ', audio_url)
        print('vk_audio_id ', vk_audio_id)
        if audio_url is None:
            audio_url = await get_music_seven(vk_audio_id)
            print('222222 (audio_url) ', audio_url)
            if audio_url is None:
                await send_message(chat_id, 'audio-not-available', lang)
                return False
    # Download and send audio
    directory = await download_vk_music(audio_url)
    print('directory: ', directory)
    audio_id = await send_audio(chat_id, open(directory, 'rb'), title=title, performer=performer, duration=duration)

    # catch error send
    if not audio_id:
        return directory
    else:
        # Save audio id to database
        if audio_id:
            files_id.set(vk_audio_id, audio_id)

        if os.path.exists(directory):
            os.remove(directory)
