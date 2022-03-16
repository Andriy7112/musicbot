# coding=utf-8
import asyncio
import json

import aiohttp


HEADERS = {'referer': 'https://kissvk.com/?search=miyagi%20fire%20man',
           'Cookie': '_ga=GA1.2.2061696967.1627409715; _ym_uid=1627409715194971199; _ym_d=1627409715; _gid=GA1.2.1240766670.1628024816; _ym_isad=2; kvk-user=%7B%22vkToken%22%3A%22ef24601265389e88e495f45744b6d2fe7064bfc97c3b69bdcb4b7a05e2856f5db097387bf2f6fe80216d4%22%2C%22vkTokenVersion%22%3A1%2C%22isGuest%22%3Afalse%2C%22initialized%22%3Afalse%2C%22id%22%3A%22619841847%22%7D; _ym_visorc=w; surfer_uuid=ca5dd46d-4e10-4577-be9b-0a857f0f694a; __gads=ID=4203467e3ebc21f9-224435f796c800a5:T=1628056592:RT=1628056592:S=ALNI_MZiyCTnZr6hA-3hJzD30FLlnoSMUQ; t_d80d2260f4=1; u_count=%5B7%2C1%5D; _gat=1; la_page_depth=%7B%22last%22%3A%22https%3A%2F%2Fkissvk.com%2F%22%2C%22depth%22%3A3%7D; u_d80d2260f4=1',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}

SEARCH_LINK = 'https://i18.kissvk.com/api/song/search/do?origin=kissvk.com&query={}' \
              '&page=0&callback=angular.callbacks._2&r=0.3983252245047464'

DOWNLOAD_URL = 'https://i{0}.kissvk.com/api/song/download/get/10/{1}-{2}-kissvk.com.mp3?origin=' \
                       'kissvk.com&url={3}&artist={1}&title={2}&index={4}&future_urls='

IPS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
       "16", "17", "18", "19", "35", "36", "37", "38", "39", "45", "46", "47", "48", "49"]


async def get_kiss_vk_music(title, performer, music_owner_id):
    search_response = await search_music(f'{title} {performer}')
    print('1) search_response: ', search_response)
    try:
        list_music_dict = search_response['songs']
    except:
        list_music_dict = None

    if not list_music_dict:
        return None

    download_url = None
    for music_dict in list_music_dict:
        if music_owner_id == music_dict['id']:
            dict_title = music_dict['title']
            dict_artist = music_dict['artist']
            dict_url = music_dict['url']
            dict_index = music_dict['index']

            download_url = await get_music(dict_title, dict_artist, dict_url, dict_index)
            return download_url

    if download_url is None:
        music_dict = list_music_dict[0]
        dict_title = music_dict['title']
        dict_artist = music_dict['artist']
        dict_url = music_dict['url']
        dict_index = music_dict['index']

        download_url = await get_music(dict_title, dict_artist, dict_url, dict_index)

    return download_url


async def search_music(song_name):
    async with aiohttp.ClientSession() as session:
        async with session.get(SEARCH_LINK.format(song_name), headers=HEADERS) as get_request:
            get_request_content = await get_request.content.read()
            content_str = str(get_request_content, 'utf-8').replace('/**/angular.callbacks._2(', '').replace(');',
                                                                                                             '')
            content_json = json.loads(content_str)

            return content_json


async def get_music(title, artist, url, index):
    for ip in IPS:
        download_url = DOWNLOAD_URL.format(ip, artist, title, url, index)
        async with aiohttp.ClientSession() as session:
            async with session.get(download_url) as get_request:
                if 'Content-Length' in get_request.headers and int(get_request.headers['Content-Length']) > 1000:
                    return download_url

    return None

if __name__ == '__main__':
    a = asyncio.run(get_kiss_vk_music('rockstar', 'post malone', '91074299_456239774'))
    print(a)
