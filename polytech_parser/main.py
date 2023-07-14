from typing import List

import config
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from collect_data import update_lists
from snils import format_snils_result, search_snils, verify_snils

bot: Bot = Bot(config.BOT_TOKEN)
dp: Dispatcher = Dispatcher()


@dp.message(Command(commands=['start']))
async def process_start_message(message: Message) -> None:
    await message.answer('Привет! Я помогу определить Ваше '
                         'место в рейтинге подавших заявления.\n /help')

@dp.message(Command(commands=['help']))
async def process_help_message(message: Message) -> None:
    await message.answer('Просто отправь СНИЛС в формате xxx-xxx-xxx xx')

@dp.message(Command(commands=['update']))
async def process_update_lists(message: Message) -> None:
    if message.from_user.username in config.admin_usernames:
        try:
            await message.answer('Списки обновляются...')
            await update_lists()
        except Exception as ex:
            await message.answer(str(ex))
        else:
            await message.answer('Списки успешно обновлены')
    else:
        await message.answer('Обновить списки может только администратор ')


@dp.message(lambda x: x.text is not None and verify_snils(x.text))
async def search_snils_in_lists(message: Message) -> None:
    search_res = search_snils(message.text)
    if search_res:
        for L in sorted(search_res, key=lambda x: x['Конкурс'][message.text]['Приоритет']):
            await message.answer(format_snils_result(message.text, L))
    else:
        await message.answer('Среди подавших заявления в политех нет человека с таким СНИЛС')

@dp.message()
async def process_another_message(message: Message) -> None:
    await message.answer('Простите, я не понимаю Вас.\n /help')


if __name__ == '__main__':
    dp.run_polling(bot)
