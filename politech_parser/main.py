import json

import asyncio
import aiohttp

from parse_directions import parse_directions
from collect_data import collect_data
import config


if __name__ == '__main__':
    async with aiohttp.ClientSession(cookies=config.cookies, headers=config.headers) as session:
        if input('Parse directionsID? y/n ') == 'y':
            asyncio.run(parse_directions(session))
        with open('directions.json', 'r', encoding='UTF-8') as file:
            directions = json.load(file)['directions']

        while code := input('Какое направление вас интересует, код?') not in directions:
            print(f'Списка для {code} нет')

        asyncio.run(collect_data(session, directions[code]['id']))
