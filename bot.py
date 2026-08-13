import os
import asyncio
import logging

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from parser import get_products


load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")


if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не задан")


if not OWNER_ID:
    raise RuntimeError("OWNER_ID не задан")


OWNER_ID = int(OWNER_ID)


bot = Bot(
    token=BOT_TOKEN
)


dp = Dispatcher()



def is_owner(message):
    return message.from_user.id == OWNER_ID



@dp.message(Command("start"))
async def start(message: Message):

    if not is_owner(message):
        await message.answer(
            "⛔ Доступ только для владельца"
        )
        return


    await message.answer(
"""
🤖 WB × OZON НАХОДКИ

Команды:

/test — проверка
/status — состояние
/post — публикация товара
/help — помощь
"""
    )



@dp.message(Command("help"))
async def help_cmd(message: Message):

    if not is_owner(message):
        return

    await message.answer(
"""
📌 Команды:

/test
/status
/post
"""
    )



@dp.message(Command("test"))
async def test(message: Message):

    if not is_owner(message):
        return


    await message.answer(
        "✅ Бот работает"
    )



@dp.message(Command("status"))
async def status(message: Message):

    if not is_owner(message):
        return


    await message.answer(
"""
🟢 Статус:

Бот запущен
WB подключен
Ozon подключен
"""
    )



@dp.message(Command("post"))
async def post(message: Message):

    if not is_owner(message):
        return


    product = get_products()


    text = f"""
🔥 НАХОДКА ДНЯ


{product['market']}


😍 {product['name']}


💰 Цена:
{product['price']}


❌ Было:
{product['old_price']}


📉 Скидка:
{product['discount']}


⭐ Рейтинг:
{product['rating']}


💬 Отзывов:
{product['reviews']}


🛒 Забрать находку:
{product['link']}


#находки #скидки #WB #OZON
"""


    await message.answer(text)



async def main():

    logging.basicConfig(
        level=logging.INFO
    )


    print("🤖 Бот запущен")


    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())
