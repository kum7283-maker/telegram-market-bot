import logging
import os
from datetime import time
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from ai_writer import generate_post
from db import init_db, save_post

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
CHANNEL_ID = os.getenv("CHANNEL_ID", "").strip()
ADMIN_ID_RAW = os.getenv("ADMIN_ID", "0").strip()
TIMEZONE = os.getenv("TIMEZONE", "Europe/Moscow")
POST_HOUR = int(os.getenv("POST_HOUR", "12"))
POST_MINUTE = int(os.getenv("POST_MINUTE", "0"))
PROXY_URL = os.getenv("PROXY_URL", "").strip()

try:
    ADMIN_ID = int(ADMIN_ID_RAW)
except ValueError:
    raise RuntimeError("ADMIN_ID must contain only digits, for example: ADMIN_ID=8401593518")

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

DEMO_PRODUCT = {
    "title": "Органайзер для дома",
    "price": 899,
    "old_price": 1990,
    "discount": 55,
    "url": "https://example.com/product",
}


def is_admin(update: Update) -> bool:
    return bool(update.effective_user and update.effective_user.id == ADMIN_ID)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        await update.message.reply_text(
            "Бот запущен. Доступ к панели есть только у владельца."
        )
        return

    await update.message.reply_text(
        "🤖 WB × OZON НАХОДКИ — панель управления\n\n"
        "/test — сделать тестовую публикацию\n"
        "/status — проверить состояние\n"
        "/post — опубликовать демо-находку\n"
        "/help — помощь"
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return
    await update.message.reply_text(
        "Первый этап готов: Telegram + автопостинг + ИИ-тексты.\n"
        "Следующим этапом подключим реальные товары WB/OZON, изображения, "
        "фильтр скидок и партнёрские ссылки."
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return

    await update.message.reply_text(
        "🟢 Конфигурация бота\n"
        f"BOT_TOKEN: {'OK' if BOT_TOKEN else 'НЕТ'}\n"
        f"CHANNEL_ID: {'OK' if CHANNEL_ID else 'НЕТ'}\n"
        f"ADMIN_ID: {'OK' if ADMIN_ID else 'НЕТ'}\n"
        f"PROXY: {'включён' if PROXY_URL else 'не задан'}\n"
        f"AI: {'включён' if os.getenv('OPENAI_API_KEY') else 'шаблонный режим'}\n"
        f"Расписание: {POST_HOUR:02d}:{POST_MINUTE:02d} ({TIMEZONE})"
    )


async def publish_demo(context: ContextTypes.DEFAULT_TYPE):
    if not CHANNEL_ID:
        logger.error("CHANNEL_ID is not configured")
        return

    product = DEMO_PRODUCT
    text = await generate_post(product)

    try:
        msg = await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=text,
            disable_web_page_preview=False,
        )
        save_post(product["url"], text, msg.message_id)
        logger.info("Published demo post: %s", msg.message_id)
    except Exception:
        logger.exception("Failed to publish post")


async def post_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return

    await update.message.reply_text("⏳ Готовлю тестовый пост...")
    await publish_demo(context)
    await update.message.reply_text("✅ Команда публикации отправлена.")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Unhandled error: %r", context.error)


def build_application():
    builder = (
        Application.builder()
        .token(BOT_TOKEN)
        .connect_timeout(20)
        .read_timeout(30)
        .write_timeout(30)
        .pool_timeout(20)
    )

    # python-telegram-bot 22.8 uses proxy() and get_updates_proxy().
    # If PROXY_URL is empty, direct connection is used.
    if PROXY_URL:
        builder = builder.proxy(PROXY_URL).get_updates_proxy(PROXY_URL)
        logger.info("Telegram proxy enabled: %s", PROXY_URL.split("@")[-1])

    return builder.build()


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set. Copy .env.example to .env and fill it.")

    if not CHANNEL_ID:
        raise RuntimeError("CHANNEL_ID is not set.")

    init_db()

    app = build_application()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("post", post_now))
    app.add_handler(CommandHandler("test", post_now))
    app.add_error_handler(error_handler)

    tz = ZoneInfo(TIMEZONE)
    app.job_queue.run_daily(
        publish_demo,
        time=time(hour=POST_HOUR, minute=POST_MINUTE, tzinfo=tz),
        name="daily_demo_post",
    )

    logger.info("Bot started")
    app.run_polling()


if __name__ == "__main__":
    main()
