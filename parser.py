import feedparser
import requests

from bs4 import BeautifulSoup


SOURCES = [

    "https://ria.ru/export/rss2/archive/index.xml",

    "https://www.m24.ru/rss.xml",

    "https://tass.ru/rss/v2.xml"

]



MOSCOW_WORDS = [

    "москва",
    "москве",
    "москвы",
    "москвой",
    "столица",
    "мэрия",
    "мосгор",
    "подмосковье"

]



IMPORTANT_WORDS = [

    "дтп",
    "пожар",
    "полиция",
    "задерж",
    "авари",
    "метро",
    "мцд",
    "мцк",
    "погода",
    "снег",
    "дожд",
    "строительство"

]





def is_moscow_news(text):


    text = text.lower()


    # Москва обязательно

    if not any(
        word in text
        for word in MOSCOW_WORDS
    ):

        return False



    return True





def get_image(url):


    try:

        r = requests.get(

            url,

            timeout=8,

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


    except:

        pass



    return None





def get_news():


    news = []



    for source in SOURCES:


        try:


            feed = feedparser.parse(

                source

            )



            for item in feed.entries[:20]:


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
                    +
                    " "
                    +
                    description

                )



                if not is_moscow_news(
                    text
                ):

                    continue



                news.append({

                    "title":
                    title,


                    "text":
                    description,


                    "link":
                    item.get(
                        "link",
                        ""
                    ),


                    "image":
                    None

                })



        except Exception as e:


            print(
                "SOURCE ERROR:",
                e
            )





    if not news:


        raise Exception(
            "Нет свежих новостей Москвы"
        )




    # берём случайную из свежих

    result = news[0]



    result["image"] = get_image(

        result["link"]

    )



    return result
