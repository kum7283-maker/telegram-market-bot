import os
import logging


from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)


from parser import get_news
from ai_writer import generate_post
from db import init_db, save_post



logging.basicConfig(
    level=logging.INFO
)



BOT_TOKEN = os.getenv(
    "BOT_TOKEN"
)


CHANNEL_ID = os.getenv(
    "CHANNEL_ID"
)



# =========================
# START
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "📰 Москва News Bot запущен\n\n"
        "/post — отправить новость\n"
        "/test — проверить канал\n"
        "/status — статус"
    )



# =========================
# STATUS
# =========================

async def status(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🟢 Бот работает\n"
        f"📢 Канал: {CHANNEL_ID}"
    )



# =========================
# TEST CHANNEL
# =========================

async def test(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text="✅ Москва News Bot работает"
        )


        await update.message.reply_text(
            "✅ Тест отправлен"
        )


    except Exception as e:

        await update.message.reply_text(
            f"❌ Ошибка:\n{e}"
        )



# =========================
# SEND NEWS
# =========================

async def send_news(
    context,
    news
):

    try:

        text = generate_post(
            news
        )


        await context.bot.send_message(

            chat_id=CHANNEL_ID,

            text=text,

            parse_mode="HTML",

            disable_web_page_preview=False

        )


        save_post(
            text
        )


        logging.info(
            "✅ Новость опубликована"
        )


    except Exception as e:


        logging.error(
            f"Ошибка отправки: {e}"
        )



# =========================
# MANUAL POST
# =========================

async def post(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:


        news = get_news()


        await send_news(

            context,

            news

        )


        await update.message.reply_text(
            "🔥 Новость опубликована"
        )



    except Exception as e:


        logging.error(
            e
        )


        await update.message.reply_text(
            f"❌ Ошибка:\n{e}"
        )



# =========================
# AUTO POST
# =========================

async def auto_post(
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        news = get_news()


        await send_news(

            context,

            news

        )


        logging.info(
            "⏰ Автопост выполнен"
        )


    except Exception as e:


        logging.error(
            f"Автопост ошибка: {e}"
        )



# =========================
# MAIN
# =========================

def main():


    init_db()



    if not BOT_TOKEN:

        raise ValueError(
            "❌ Нет BOT_TOKEN"
        )


    if not CHANNEL_ID:

        raise ValueError(
            "❌ Нет CHANNEL_ID"
        )



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



    # Автопубликация каждые 2 часа

    if app.job_queue:


        app.job_queue.run_repeating(

            auto_post,

            interval=7200,

            first=120

        )


        logging.info(
            "⏰ Автопост включён"
        )


    else:

        logging.warning(
            "JobQueue отсутствует"
        )



    logging.info(
        "📰 БОТ ЗАПУЩЕН"
    )


    app.run_polling()



if __name__ == "__main__":

    main()
