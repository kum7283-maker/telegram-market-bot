import requests
import random


def get_product():

    query = random.choice([
        "телефон",
        "наушники",
        "кроссовки",
        "робот пылесос",
        "часы",
        "товары для дома"
    ])

    url = "https://search.wb.ru/exactmatch/ru/search/v4/search"

    params = {
        "ab_testing": "false",
        "appType": "1",
        "curr": "rub",
        "dest": "-1257786",
        "query": query,
        "resultset": "catalog",
        "page": "1",
        "sort": "popular"
    }

    headers = {
        "User-Agent":
        "Mozilla/5.0",
        "Accept":
        "application/json",
        "Referer":
        "https://www.wildberries.ru/"
    }


    try:

        r = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=20
        )


        print("WB STATUS:", r.status_code)
        print(r.text[:200])


        data = r.json()


        products = data.get(
            "data",
            {}
        ).get(
            "products",
            []
        )


        if len(products) == 0:
            raise Exception(
                "WB пустой ответ"
            )


        p = random.choice(products)


        article = p["id"]

        price = p.get(
            "salePriceU",
            0
        ) // 100

        old = p.get(
            "priceU",
            0
        ) // 100


        img = (
            "https://basket-"
            + str(article // 100000)
            + ".wbbasket.ru/"
            "vol"
            + str(article // 100000)
            + "/part"
            + str(article // 1000)
            + "/"
            + str(article)
            + "/images/big/1.webp"
        )


        return {

            "market":
            "🟣 Wildberries",

            "article":
            article,

            "name":
            p.get("name"),

            "price":
            f"{price} ₽",

            "old_price":
            f"{old} ₽",

            "discount":
            str(
                p.get(
                    "sale",
                    0
                )
            ) + "%",

            "rating":
            str(
                p.get(
                    "rating",
                    0
                )
            ),

            "reviews":
            str(
                p.get(
                    "feedbacks",
                    0
                )
            ),

            "link":
            f"https://www.wildberries.ru/catalog/{article}/detail.aspx",

            "image":
            img
        }


    except Exception as e:

        print(
            "WB ERROR:",
            e
        )

        return {

            "market":
            "🟣 Wildberries",

            "article":
            "0",

            "name":
            "Ошибка WB",

            "price":
            "0 ₽",

            "old_price":
            "0 ₽",

            "discount":
            "0%",

            "rating":
            "0",

            "reviews":
            "0",

            "link":
            "https://www.wildberries.ru",

            "image":
            None
        }
