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



BOT_TOKEN=os.getenv(
    "BOT_TOKEN"
)


CHANNEL_ID=os.getenv(
    "CHANNEL_ID"
)




async def start(
    update:Update,
    context:ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "📰 Москва News Bot работает"
    )





async def publish(
    context,
    news
):


    text = generate_post(
        news
    )


    image = news.get(
        "image"
    )


    if image:


        await context.bot.send_photo(

            chat_id=CHANNEL_ID,

            photo=image,

            caption=text,

            parse_mode="HTML"

        )


    else:


        await context.bot.send_message(

            chat_id=CHANNEL_ID,

            text=text,

            parse_mode="HTML"

        )


    save_post(
        text
    )





async def post(
    update,
    context
):


    news=get_news()


    await publish(
        context,
        news
    )


    await update.message.reply_text(
        "✅ Новость опубликована"
    )





async def auto_post(
    context
):


    try:

        news=get_news()

        await publish(
            context,
            news
        )


        print(
            "NEWS OK"
        )


    except Exception as e:


        print(
            e
        )





def main():


    init_db()


    app=(

        Application

        .builder()

        .token(
            BOT_TOKEN
        )

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
            "post",
            post
        )

    )



    app.job_queue.run_repeating(

        auto_post,

        interval=1800,

        first=60

    )



    print(
        "MOSCOW NEWS START"
    )


    app.run_polling()




if __name__=="__main__":

    main()
