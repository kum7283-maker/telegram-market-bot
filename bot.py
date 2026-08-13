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


# =========================
# START
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🤖 WB × OZON НАХОДКИ\n\n"
        "/post — опубликовать товар\n"
        "/test — проверить канал\n"
        "/status — проверить состояние"
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
# TEST
# =========================

async def test(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text="✅ Тестовая публикация работает"
        )

        await update.message.reply_text(
            "✅ Тест отправлен в канал"
        )

    except Exception as e:

        logging.error(e)

        await update.message.reply_text(
            f"❌ Ошибка отправки в канал:\n{e}"
        )


# =========================
# ОТПРАВКА ТОВАРА
# =========================

async def send_product(
    context: ContextTypes.DEFAULT_TYPE,
    product: dict
):

    text = generate_post(product)

    video = product.get("video")
    image = product.get("image")


    # =========================
    # ЕСЛИ ЕСТЬ ВИДЕО
    # =========================

    if video:

        try:

            await context.bot.send_video(
                chat_id=CHANNEL_ID,
                video=video,
                caption=text
            )

            logging.info(
                "Видео товара опубликовано"
            )

        except Exception as e:

            logging.error(
                f"Ошибка отправки видео: {e}"
            )

            # если видео не загрузилось,
            # пробуем отправить фото

            if image:

                await context.bot.send_photo(
                    chat_id=CHANNEL_ID,
                    photo=image,
                    caption=text
                )

            else:

                await context.bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=text
                )


    # =========================
    # ЕСЛИ ЕСТЬ ФОТО
    # =========================

    elif image:

        await context.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=image,
            caption=text
        )

        logging.info(
            "Фото товара опубликовано"
        )


    # =========================
    # ЕСЛИ НЕТ МЕДИА
    # =========================

    else:

        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=text
        )

        logging.info(
            "Товар опубликован без медиа"
        )


    # сохраняем текст поста
    save_post(text)


# =========================
# РУЧНОЙ POST
# =========================

async def post(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        product = get_product()

        await send_product(
            context,
            product
        )

        await update.message.reply_text(
            "🔥 Товар опубликован в канал"
        )

    except Exception as e:

        logging.error(
            f"Post error: {e}"
        )

        await update.message.reply_text(
            f"❌ Ошибка:\n{e}"
        )


# =========================
# АВТОПОСТ
# =========================

async def auto_post(
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        product = get_product()

        await send_product(
            context,
            product
        )

        logging.info(
            "✅ Автоматический пост опубликован"
        )

    except Exception as e:

        logging.error(
            f"Auto post error: {e}"
        )


# =========================
# MAIN
# =========================

def main():

    init_db()


    if not BOT_TOKEN:

        raise ValueError(
            "Не найдена переменная BOT_TOKEN"
        )


    if not CHANNEL_ID:

        raise ValueError(
            "Не найдена переменная CHANNEL_ID"
        )


    app = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )


    # Команды

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


    # =========================
    # АВТОПУБЛИКАЦИЯ
    # =========================
    #
    # Первый пост через 60 секунд
    # Далее каждые 2 часа
    #

    if app.job_queue:

        app.job_queue.run_repeating(
            auto_post,
            interval=7200,
            first=60
        )

    else:

        logging.warning(
            "JobQueue недоступен. "
            "Проверь python-telegram-bot[job-queue]"
        )


    print("🤖 BOT STARTED")


    app.run_polling()


# =========================
# START PROGRAM
# =========================

if __name__ == "__main__":

    main()
