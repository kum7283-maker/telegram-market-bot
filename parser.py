import requests
import random


CATEGORIES = [
    "товары для дома",
    "электроника",
    "автотовары",
    "инструменты",
    "одежда"
]


def get_product():

    category = random.choice(CATEGORIES)

    search_url = "https://search.wb.ru/exactmatch/ru/common/v4/search"


    params = {
        "query": category,
        "resultset": "catalog",
        "sort": "popular",
        "page": 1
    }


    headers = {
        "User-Agent": "Mozilla/5.0"
    }


    try:

        r = requests.get(
            search_url,
            params=params,
            headers=headers,
            timeout=15
        )


        data = r.json()

        products = data["data"]["products"]


        product = random.choice(products)


        article = product["id"]


        name = product.get(
            "name",
            "Товар WB"
        )


        price = product.get(
            "salePriceU",
            0
        ) // 100


        old_price = product.get(
            "priceU",
            0
        ) // 100


        discount = 0

        if old_price > 0:
            discount = round(
                (1 - price / old_price) * 100
            )


        # данные для картинки
        vol = product.get("vol")
        part = product.get("part")
        root = product.get("root")


        image = None


        if vol and part and root:

            image = (
                f"https://basket-01.wbbasket.ru/"
                f"vol{vol}/part{part}/"
                f"{root}/images/big/1.webp"
            )


        return {

            "market": "🟣 Wildberries",

            "article": str(article),

            "name": name,

            "price": f"{price} ₽",

            "old_price": f"{old_price} ₽",

            "discount": f"{discount}%",

            "rating": str(
                product.get(
                    "rating",
                    "Нет"
                )
            ),

            "reviews": str(
                product.get(
                    "feedbacks",
                    0
                )
            ),

            "link":
            f"https://www.wildberries.ru/catalog/{article}/detail.aspx",

            "image": image,

            "video": None
        }


    except Exception as e:

        print("WB ERROR:", e)


        return {

            "market": "🟣 Wildberries",
            "article": "нет",
            "name": "Ошибка",
            "price": "0 ₽",
            "old_price": "0 ₽",
            "discount": "0%",
            "rating": "0",
            "reviews": "0",
            "link": "https://www.wildberries.ru",
            "image": None,
            "video": None
        }
