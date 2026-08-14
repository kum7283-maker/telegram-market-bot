import os
from telethon import TelegramClient


API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")


client = TelegramClient(
    "moscow_session",
    API_ID,
    API_HASH
)


CHANNELS = [

    "moscowach",
    "moscowmap",
    "moscowachannel"

]


MOSCOW_WORDS = [

    "москва",
    "москве",
    "москвы",
    "мкад",
    "метро",
    "мцд",
    "мцк",
    "ттк"

]



async def get_telegram_news():


    await client.start()


    news = []


    for channel in CHANNELS:


        try:


            entity = await client.get_entity(
                channel
            )


            messages = await client.get_messages(
                entity,
                limit=5
            )


            for msg in messages:


                if not msg.text:

                    continue


                text = msg.text.lower()


                if not any(
                    x in text
                    for x in MOSCOW_WORDS
                ):

                    continue



                image = None


                if msg.photo:


                    image = await msg.download_media()



                news.append({

                    "title":
                    msg.text[:120],


                    "text":
                    msg.text,


                    "link":
                    f"https://t.me/{channel}/{msg.id}",


                    "image":
                    image

                })


        except Exception as e:


            print(
                "TG ERROR:",
                e
            )



    if not news:


        raise Exception(
            "Нет новостей Telegram"
        )


    return news[0]
