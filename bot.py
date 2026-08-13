import os
import asyncio
import logging

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from parser import get_wb_products


# =====================
# НАСТРОЙКИ
# =====================

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")


if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не задан")


if not OWNER_ID:
    raise RuntimeError("OWNER_ID не задан")


OWNER_ID = int(OWNER_ID)


# =====================
# БОТ
# =====================

bot = Bot(
    token=BOT_TOKEN
)

dp = Dispatcher()


# =====================
# ПРОВЕРКА ВЛАДЕЛЬЦА
# =====================

def is_owner(message: Message):
    return message.from_user.id == OWNER_ID



# =====================
# START
# =====================

@dp.message(Command("start"))
async def start(message: Message):

    if not is_owner(message):
        await message.answer(
            "⛔ Доступ к панели есть только у владельца."
        )
        return


    await message.answer(
        """
🤖 WB × OZON НАХОДКИ — панель управления


Команды:

/test — проверка бота
/status — состояние
/post — публикация товара
/help — помощь
"""
    )



# =====================
# HELP
# =====================

@dp.message(Command("help"))
async def help_cmd(message: Message):

    if not is_owner(message):
        return


    await message.answer(
        """
📌 Управление ботом:

/test — тест
/status — статус
/post — найти товар
"""
    )



# =====================
# TEST
# =====================

@dp.message(Command("test"))
async def test(message: Message):

    if not is_owner(message):
        return


    await message.answer(
        "✅ Бот работает"
    )



# =====================
# STATUS
# =====================

@dp.message(Command("status"))
async def status(message: Message):

    if not is_owner(message):
        return


    await message.answer(
        """
🟢 Статус:

Бот запущен
Парсер WB подключен
AI модуль готов
"""
    )



# =====================
# POST
# =====================

@dp.message(Command("post"))
async def post(message: Message):

    if not is_owner(message):
        return


    product = get_wb_products()


    text = f"""
🔥 НАХОДКА ДНЯ


🛒 {product['name']}


🏪 Маркетплейс:
{product['market']}


💰 Цена:
{product['price']}

❌ Старая цена:
{product['old_price']}


⭐ Рейтинг:
{product['rating']}

💬 Отзывов:
{product['reviews']}


📂 Категория:
{product['category']}


🔗 Ссылка:
{product['url']}


#находка #WB #OZON
"""


    await message.answer(text)



# =====================
# ЗАПУСК
# =====================

async def main():

    logging.basicConfig(
        level=logging.INFO
    )


    print("🤖 Бот запущен")


    await dp.start_polling(bot)



if __name__ == "__main__":

    asyncio.run(main())
