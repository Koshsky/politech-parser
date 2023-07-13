import json

import asyncio
import aiohttp

from parse_directions import parse_directions
from collect_data import collect_all_data
import config

async def main():
    async with aiohttp.ClientSession(cookies=config.cookies, headers=config.headers) as session:
        asyncio.run(parse_directions(session))

        with open('directions.json', 'r', encoding='UTF-8') as file:
            directions = json.load(file)['directions']

        await collect_all_data(session)

if __name__ == '__main__':
    asyncio.run(main())