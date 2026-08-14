import feedparser
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime


SOURCES = [

    "https://ria.ru/export/rss2/archive/index.xml",

    "https://tass.ru/rss/v2.xml",

    "https://www.m24.ru/rss.xml"

]




def get_image(url):

    try:

        r = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )


        soup = BeautifulSoup(
            r.text,
            "html.parser"
        )


        img = soup.find(
            "meta",
            property="og:image"
        )


        if img:

            return img.get(
                "content"
            )


    except Exception:

        pass


    return None





def get_news():


    news_list = []



    for source in SOURCES:


        try:


            feed = feedparser.parse(
                source
            )


            for item in feed.entries[:10]:


                title = item.get(
                    "title",
                    ""
                )


                description = item.get(
                    "description",
                    ""
                )


                link = item.get(
                    "link",
                    ""
                )



                if not title:

                    continue



                news_list.append({

                    "title":
                    title,

                    "text":
                    description,

                    "link":
                    link,

                    "image":
                    None,

                    "time":
                    item.get(
                        "published",
                        ""
                    )

                })



        except Exception as e:


            print(
                "RSS ERROR",
                e
            )




    if not news_list:


        raise Exception(
            "Новостей нет"
        )



    # выбираем свежую


    news = random.choice(
        news_list[:10]
    )



    # ищем картинку


    news["image"] = get_image(
        news["link"]
    )



    return news
