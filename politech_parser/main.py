import json
from pprint import pprint

import asyncio
import aiohttp

from parse_directions import parse_directions
from collect_data import collect_all_data
from snils import search_snils, snils_in_list
import config

async def parse():
    async with aiohttp.ClientSession(cookies=config.cookies, headers=config.headers) as session:
        await parse_directions(session)

        with open('directions.json', 'r', encoding='UTF-8') as file:
            directions = json.load(file)['directions']

        await collect_all_data(session)


if __name__ == '__main__':
    if input('Обновить списки подавших заявление? y/n ') == 'y':
        asyncio.run(parse())
        print('Собраны актуальные списки')
    with open('parsed_data/SNILSES.txt', 'r') as file:
        SNILSES = [i.strip() for i in file]

    while (snils := input('Введите СНИЛС в формате xxx-xxx-xxx xx: ')) not in SNILSES:
        print('Попробуйте еще раз')
    search_res = search_snils(snils)
    for i in search_res:
        print(snils)
        print(snils_in_list(snils, i))
