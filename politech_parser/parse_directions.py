import json
import asyncio

from aiohttp_retry import RetryClient, ExponentialRetry
import aiohttp


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0',
    'Accept': '*/*',
    'Accept-Language': 'ru',
    'Referer': 'https://enroll.spbstu.ru/',
    'authorization': 'Bearer eyJqa3UiOiJodHRwczovL2Vucm9sbC5zcGJzdHUucnUvdXNlci1tYW5hZ2VyL2FwaS92MS9hdXRoL2p3a3MiLCJraWQiOiI0ODczMmQ0Yi1jN2RlLTRlM2YtOGVkNi1kODRmZjZmZGNkZTciLCJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJ1c2VySWQiOjIwNjQ4LCJyb2xlIjoiVVNFUiIsInByZWZMYW5nIjoicnUiLCJleHAiOjE2ODkyODE1MjcsImlhdCI6MTY4OTI0NTUyNywidHlwIjoiQUNDRVNTIn0.L7wl2xoQiMZw_RvQtQQ3i1I3KeirX79kFGHdJs7IHiedVGCTIwqr4MSG06X6MF2DrLgB3CSVtmnGU7O87s0E5Q',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}


cookies = {
    '__utma': '140980720.2019465368.1689105479.1689105479.1689245519.2',
    '__utmz': '140980720.1689245519.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
    'JSESSIONID': '4AA78DE10D595C3EF7D99341B4F5DA5D',
    '_ga': 'GA1.2.2019465368.1689105479',
    '_ga_ZDPCMGYF85': 'GS1.2.1689174793.1.1.1689174802.0.0.0',
    '__utmc': '140980720',
    'session-cookie': '177167dafb23f1e3e9cec56db4b53d11cc1665b4391711dbb344e5fd3ddb977d62e06da72d4cb1a4c560d695db8784d4',
}

JSON = {'directions': {}}

async def collect_directiondID(session: aiohttp.ClientSession, search: str):
    params = {
    'name': search,
    'educationFormId': '2',
    'educationLevelId': '2,5',
    'admissionBasis': 'BUDGET',
    'showClosed': 'true',
    }
    url = 'https://enroll.spbstu.ru/applications-manager/api/v1/directions/all-pageable'
    retry_options = ExponentialRetry(attempts=5)
    retry_client = RetryClient(raise_for_status=False, retry_options=retry_options, client_session=session,
                               start_timeout=0.5)
    async with retry_client.get(url, params=params) as response:
        if response.ok:
            resp = await response.json()
            for i in resp['result']:
                JSON['directions'][i['code']] = {
                    'title': i['title'],
                    'id': i['id']
                }


async def parse_directions():
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        tasks = []
        for i in map(lambda x: str(x).zfill(2), range(1, 99)):
            task = asyncio.create_task(collect_directiondID(session, i))
            tasks.append(task)
        await asyncio.gather(*tasks)
    with open('directions.json', 'w', encoding='UTF-8') as file:
        json.dump(JSON, file, indent=4, ensure_ascii=False)



if __name__ == '__main__':
    asyncio.run(parse_directions())
