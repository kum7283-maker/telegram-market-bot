import os
import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from parser import get_product
from ai_writer import generate_post
from db import init_db, save_post


logging.basicConfig(
    level=logging.INFO
)


BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
ADMIN_ID = os.getenv("ADMIN_ID")


# =========================
# Команда /start
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🤖 WB & Ozon Market Bot запущен\n\n"
        "/post — создать пост\n"
        "/test — проверить канал\n"
        "/status — статус"
    )


# =========================
# Тест отправки в канал
# =========================

async def test(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text="✅ Тестовое сообщение от бота"
    )

    await update.message.reply_text(
        "Тест отправлен в канал"
    )


# =========================
# Создание поста
# =========================

async def post(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        product = get_product()

        text = generate_post(product)


        # отправка именно в канал
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=text
        )


        # сохранение в базу
        save_post(text)


        await update.message.reply_text(
            "✅ Пост опубликован в канал"
        )


    except Exception as e:

        logging.error(e)

        await update.message.reply_text(
            f"❌ Ошибка:\n{e}"
        )


# =========================
# Статус
# =========================

async def status(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🟢 Бот работает\n"
        f"Канал: {CHANNEL_ID}"
    )


# =========================
# Запуск
# =========================

def main():

    init_db()


    app = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CommandHandler(
            "test",
            test
        )
    )


    app.add_handler(
        CommandHandler(
            "post",
            post
        )
    )


    app.add_handler(
        CommandHandler(
            "status",
            status
        )
    )


    print("BOT STARTED")


    app.run_polling()



if __name__ == "__main__":
    main()
