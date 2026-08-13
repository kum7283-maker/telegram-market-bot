import requests
import random


def get_product():

    categories = [
        "elektronika",
        "dom",
        "krasota",
        "sport",
        "odezhda",
        "avto"
    ]

    category = random.choice(categories)

    url = "https://search.wb.ru/exactmatch/ru/common/v4/search"

    params = {
        "query": category,
        "resultset": "catalog",
        "page": 1,
        "appType": 1,
        "curr": "rub",
        "dest": -1257786
    }

    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept":
        "application/json"
    }


    try:

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=20
        )


        if response.status_code != 200:
            raise Exception(
                f"WB ошибка {response.status_code}"
            )


        data = response.json()


        products = data.get(
            "data",
            {}
        ).get(
            "products",
            []
        )


        if not products:
            raise Exception(
                "Товары не найдены"
            )


        product = random.choice(products)


        article = product.get(
            "id"
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

        if old_price:
            discount = round(
                100 - (price / old_price * 100)
            )


        image = (
            f"https://basket-{article//100000}.wbbasket.ru/"
            f"vol{article//100000}/part{article//1000}/"
            f"{article}/images/big/1.webp"
        )


        return {

            "market":
            "🟣 Wildberries",

            "article":
            article,

            "name":
            product.get(
                "name",
                "Без названия"
            ),

            "price":
            f"{price} ₽",

            "old_price":
            f"{old_price} ₽",

            "discount":
            f"{discount}%",

            "rating":
            str(
                product.get(
                    "rating",
                    0
                )
            ),

            "reviews":
            str(
                product.get(
                    "feedbacks",
                    0
                )
            ),

            "link":
            f"https://www.wildberries.ru/catalog/{article}/detail.aspx",

            "image":
            image,

            "video":
            None

        }


    except Exception as e:

        print("PARSER ERROR:", e)

        return {

            "market":
            "🟣 Wildberries",

            "article":
            "0",

            "name":
            f"Ошибка: {e}",

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
            None,

            "video":
            None
        }
