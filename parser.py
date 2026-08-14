import requests
import feedparser
import random
from bs4 import BeautifulSoup


# Источники новостей
SOURCES = [
    "https://www.mos.ru/rss/news/",
    "https://tass.ru/rss/v2.xml",
    "https://ria.ru/export/rss2/archive/index.xml"
]


KEYWORDS = [
    "Москва",
    "москв",
    "Московская область",
    "метро",
    "МКАД",
    "МЦК",
    "транспорт",
    "улица",
    "район"
]


def check_moscow(text):

    text = text.lower()

    for word in KEYWORDS:
        if word.lower() in text:
            return True

    return False



def clean_text(text):

    soup = BeautifulSoup(
        text,
        "html.parser"
    )

    return soup.get_text(
        " ",
        strip=True
    )



def get_news():

    news = []


    for source in SOURCES:

        try:

            feed = feedparser.parse(source)


            for item in feed.entries[:10]:

                title = item.get(
                    "title",
                    ""
                )

                description = item.get(
                    "description",
                    ""
                )


                text = (
                    title
                    + " "
                    + description
                )


                text = clean_text(text)


                if check_moscow(text):

                    news.append({

                        "title":
                        title,

                        "text":
                        text,

                        "link":
                        item.get(
                            "link",
                            ""
                        ),

                        "source":
                        source

                    })


        except Exception as e:

            print(
                "RSS ERROR:",
                e
            )


    if len(news) == 0:

        return {

            "title":
            "Новостей нет",

            "text":
            "Новости Москвы не найдены",

            "link":
            "",

            "source":
            ""

        }


    return random.choice(news)
