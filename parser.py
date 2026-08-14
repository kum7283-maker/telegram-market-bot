import feedparser
import random
import requests
from bs4 import BeautifulSoup


SOURCES = [

    "https://www.mos.ru/rss/news/",

    "https://ria.ru/export/rss2/archive/index.xml",

    "https://tass.ru/rss/v2.xml"

]


KEYWORDS = [

    "Москва",
    "москв",
    "метро",
    "МКАД",
    "МЦК",
    "транспорт",
    "улица",
    "район"

]



def is_moscow(text):

    text = text.lower()

    for word in KEYWORDS:

        if word.lower() in text:

            return True

    return False



def clean(text):

    soup = BeautifulSoup(
        text,
        "html.parser"
    )

    return soup.get_text(
        " ",
        strip=True
    )



def get_image(entry):

    try:

        if "media_content" in entry:

            return entry.media_content[0]["url"]


        if "media_thumbnail" in entry:

            return entry.media_thumbnail[0]["url"]


        if "enclosures" in entry:

            return entry.enclosures[0]["url"]


    except:

        pass


    return None




def get_news():


    news_list = []


    for url in SOURCES:


        try:

            feed = feedparser.parse(url)


            for item in feed.entries[:10]:


                title = item.get(
                    "title",
                    ""
                )


                description = item.get(
                    "description",
                    ""
                )


                text = clean(
                    title +
                    " " +
                    description
                )


                if is_moscow(text):


                    news_list.append({

                        "title": title,

                        "text": text,

                        "link":
                        item.get(
                            "link",
                            ""
                        ),

                        "image":
                        get_image(item)

                    })


        except Exception as e:

            print(
                "SOURCE ERROR:",
                e
            )



    if not news_list:


        return {

            "title":
            "Новости Москвы",

            "text":
            "Новых новостей нет",

            "link":
            "",

            "image":
            None

        }



    return random.choice(
        news_list
    )
