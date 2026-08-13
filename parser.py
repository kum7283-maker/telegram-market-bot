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

    url = "https://search.wb.ru/exactmatch/ru/common/v4/search"

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

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=15
        )


        data = response.json()


        products = data["data"]["products"]


        # берём товар с картинкой
        products = [
            p for p in products
            if p.get("id")
        ]


        product = random.choice(products)


        article = product.get("id")


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



        if old_price > 0:

            discount = round(
                (1 - price / old_price) * 100
            )

        else:

            discount = 0



        # данные для фото WB

        root = product.get(
            "root"
        )

        vol = product.get(
            "vol"
        )

        part = product.get(
            "part"
        )

        basket = product.get(
            "basket"
        )


        image = None


        if root and vol and part and basket:

            image = (
                f"https://basket-{basket}.wbbasket.ru/"
                f"vol{vol}/part{part}/"
                f"{root}/images/big/1.webp"
            )


        link = (
            f"https://www.wildberries.ru/catalog/"
            f"{article}/detail.aspx"
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

            "link": link,

            "image": image,

            "video": None
        }



    except Exception as e:

        print(
            "WB PARSER ERROR:",
            e
        )


        return {

            "market": "🟣 Wildberries",

            "article": "нет",

            "name": "Ошибка получения товара",

            "price": "0 ₽",

            "old_price": "0 ₽",

            "discount": "0%",

            "rating": "0",

            "reviews": "0",

            "link": "https://www.wildberries.ru",

            "image": None,

            "video": None
        }
