import requests
import random


# Категории WB
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
        "User-Agent":
        "Mozilla/5.0"
    }


    try:

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )


        data = response.json()


        products = data["data"]["products"]


        # выбираем случайный товар
        product = random.choice(products)


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


        article = product.get(
            "id"
        )


        link = (
            f"https://www.wildberries.ru/catalog/{article}/detail.aspx"
        )


        # фото
        image = (
            f"https://basket-{product.get('basket')}.wbbasket.ru/"
            f"vol{article//100000}/part{article//1000}/"
            f"{article}/images/big/1.webp"
        )


        return {

            "market": "🟣 Wildberries",

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

            "image": image
        }



    except Exception as e:


        print(
            "WB ERROR:",
            e
        )


        # запасной вариант
        return {

            "market": "🟣 Wildberries",

            "name": "Популярный товар дня",

            "price": "999 ₽",

            "old_price": "1999 ₽",

            "discount": "50%",

            "rating": "4.8",

            "reviews": "5000",

            "link": "https://www.wildberries.ru",

            "image": None
        }
