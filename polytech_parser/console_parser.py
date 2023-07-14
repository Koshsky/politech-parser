import asyncio
import json
import os

from collect_data import update_lists
from snils import format_snils_result, search_snils, verify_snils

if __name__ == '__main__':
    if input('Обновить списки подавших заявление? y/n ') == 'y':
        asyncio.run(update_lists())
        print('Собраны актуальные списки')

    while not verify_snils(snils := input('Введите СНИЛС в формате xxx-xxx-xxx xx: ')):
        print('Попробуйте еще раз')
    search_res = search_snils(snils)

    if search_res:
        for list_ in search_res:
            print(format_snils_result(snils, list_))
    else:
        print('Среди подавших заявления в политех нет человека с таким СНИЛСом')
