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

    try:

        category = random.choice(CATEGORIES)


        url = "https://search.wb.ru/exactmatch/ru/common/v4/search"


        params = {
            "query": category,
            "resultset": "catalog",
            "sort": "popular",
            "page": 1
        }


        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Referer": "https://www.wildberries.ru/"
        }


        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=20
        )


        print("WB STATUS:", response.status_code)


        data = response.json()


        products = (
            data
            .get("data", {})
            .get("products", [])
        )


        if not products:

            raise Exception(
                "WB вернул пустой список товаров"
            )


        product = random.choice(products)


        article = product.get("id")


        price = (
            product.get(
                "salePriceU",
                0
            )
            // 100
        )


        old_price = (
            product.get(
                "priceU",
                0
            )
            // 100
        )


        discount = 0

        if old_price and price:

            discount = round(
                (1 - price / old_price) * 100
            )


        image = None


        if product.get("id"):

            image = (
                f"https://images.wbstatic.net/"
                f"big/new/{article//10000}/"
                f"{article}-1.jpg"
            )


        return {

            "market": "🟣 Wildberries",

            "article": str(article),

            "name": product.get(
                "name",
                "Товар WB"
            ),

            "price": f"{price} ₽",

            "old_price": f"{old_price} ₽",

            "discount": f"{discount}%",

            "rating": str(
                product.get(
                    "rating",
                    "нет"
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
            repr(e)
        )


        return {

            "market": "🟣 Wildberries",

            "article": "ошибка",

            "name": f"Ошибка WB: {e}",

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
