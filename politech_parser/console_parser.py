import json

import asyncio
import aiohttp

from parse_directions import parse_directions
from collect_data import collect_all_data
from snils import search_snils, snils_in_list, verify_snils
import config

async def update_lists():
    async with aiohttp.ClientSession(cookies=config.cookies, headers=config.headers) as session:
        await parse_directions(session)

        with open('directions.json', 'r', encoding='UTF-8') as file:
            directions = json.load(file)['directions']

        await collect_all_data(session)


if __name__ == '__main__':
    if input('Обновить списки подавших заявление? y/n ') == 'y':
        asyncio.run(update_lists())
        print('Собраны актуальные списки')
    with open('parsed_data/SNILSES.txt', 'r') as file:
        SNILSES = [i.strip() for i in file]

    while not verify_snils(snils := input('Введите СНИЛС в формате xxx-xxx-xxx xx: ')):
        print('Попробуйте еще раз')
    search_res = search_snils(snils)
    if search_res:
        for L in search_res:
            print(snils_in_list(snils, L))
    else:
        print('Среди подавших заявления в политех нет человека с таким СНИЛСом')
