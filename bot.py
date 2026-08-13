import os
import logging

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from parser import get_product
from ai_writer import generate_post
from db import init_db, save_post


load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")


logging.basicConfig(
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🤖 WB × OZON НАХОДКИ\n\n"
        "/test — тестовая публикация\n"
        "/post — отправить находку\n"
        "/status — состояние"
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "✅ Бот работает"
    )


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):

    product = get_product()

    text = generate_post(product)

    await update.message.reply_text(text)



async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):

    product = get_product()

    text = generate_post(product)

    save_post(text)


    if CHANNEL_ID:

        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=text
        )

    else:

        await update.message.reply_text(text)



def main():

    init_db()


    app = Application.builder()\
        .token(BOT_TOKEN)\
        .build()


    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("test", test)
    )

    app.add_handler(
        CommandHandler("post", post)
    )

    app.add_handler(
        CommandHandler("status", status)
    )


    print("BOT STARTED")


    app.run_polling()



if __name__ == "__main__":
    main()
