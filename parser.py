import requests
import random


CATEGORIES = [
    "товары для дома",
    "электроника",
    "авто",
    "инструменты",
    "одежда"
]


def get_product():

    category = random.choice(CATEGORIES)

    url = "https://search.wb.ru/exactmatch/ru/common/v5/search"


    params = {
        "query": category,
        "resultset": "catalog",
        "page": 1,
        "sort": "popular"
    }


    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }


    try:

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=20
        )


        response.raise_for_status()


        data = response.json()


        products = (
            data
            .get("data", {})
            .get("products", [])
        )


        if not products:

            raise Exception(
                "Товары WB не найдены"
            )


        product = random.choice(products)


        article = product.get("id")


        name = product.get(
            "name",
            "Товар WB"
        )


        price = (
            product.get(
                "salePriceU",
                0
            ) // 100
        )


        old_price = (
            product.get(
                "priceU",
                0
            ) // 100
        )


        discount = 0

        if old_price > 0 and price > 0:

            discount = round(
                (1 - price / old_price) * 100
            )


        # картинка WB

        image = None


        if article:

            image = (
                f"https://basket-01.wbbasket.ru/"
                f"vol{article//100000}/"
                f"part{article//1000}/"
                f"{article}/images/big/1.webp"
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

        print(
            "WB ERROR:",
            e
        )


        # чтобы бот не падал

        return {

            "market": "🟣 Wildberries",

            "article": "нет",

            "name": "Не удалось получить товар",

            "price": "0 ₽",

            "old_price": "0 ₽",

            "discount": "0%",

            "rating": "0",

            "reviews": "0",

            "link":
            "https://www.wildberries.ru",

            "image": None,

            "video": None
        }
