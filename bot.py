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


# ==========================
# Старт
# ==========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🤖 WB × OZON НАХОДКИ\n\n"
        "/post — опубликовать находку\n"
        "/test — тест канала\n"
        "/status — статус"
    )


# ==========================
# Статус
# ==========================

async def status(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🟢 Бот работает\n"
        f"Канал: {CHANNEL_ID}"
    )


# ==========================
# Тест отправки
# ==========================

async def test(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text="✅ Тестовая публикация работает"
    )


    await update.message.reply_text(
        "✅ Проверка отправлена в канал"
    )


# ==========================
# Ручной пост
# ==========================

async def post(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        product = get_product()

        text = generate_post(product)


        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=text
        )


        save_post(text)


        await update.message.reply_text(
            "🔥 Находка опубликована"
        )


    except Exception as e:

        logging.error(e)

        await update.message.reply_text(
            f"Ошибка: {e}"
        )


# ==========================
# Автоматическая публикация
# ==========================

async def auto_post(
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        product = get_product()

        text = generate_post(product)


        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=text
        )


        save_post(text)


        logging.info(
            "Автопост опубликован"
        )


    except Exception as e:

        logging.error(
            f"Auto post error: {e}"
        )


# ==========================
# Запуск
# ==========================

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
            "status",
            status
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


    # Автопост каждые 2 часа
    app.job_queue.run_repeating(
        auto_post,
        interval=7200,
        first=30
    )


    print("BOT STARTED")


    app.run_polling()



if __name__ == "__main__":
    main()
