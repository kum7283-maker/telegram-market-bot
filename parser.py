import feedparser
import random


SOURCES = [

    "https://ria.ru/export/rss2/archive/index.xml",

    "https://www.m24.ru/rss.xml",

    "https://www.interfax.ru/rss.asp",

]


KEYWORDS = [

    "Москва",
    "москве",
    "москвы",
    "мэр",
    "метро",
    "ДТП",
    "полиция",
    "пожар",
    "погода"

]


def get_news():


    random.shuffle(SOURCES)


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


                text = title + " " + description


                if any(
                    word.lower() in text.lower()
                    for word in KEYWORDS
                ):


                    image = None


                    if hasattr(
                        item,
                        "media_content"
                    ):

                        image = item.media_content[0].get(
                            "url"
                        )


                    return {

                        "title": title,

                        "text": description,

                        "link": item.get(
                            "link",
                            ""
                        ),

                        "image": image

                    }


        except Exception as e:

            print(
                "RSS ERROR",
                e
            )


    return {

        "title":
        "Новости Москвы",

        "text":
        "Свежие новости города",

        "link":
        "",

        "image":
        None

    }
