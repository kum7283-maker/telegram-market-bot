import requests
import random


ARTICLES = [
    183126859,
    145774392,
    219739888,
    168542331,
    234567891
]


def get_product():

    article = random.choice(ARTICLES)


    url = (
        "https://card.wb.ru/cards/v2/detail"
    )


    params = {
        "appType": 1,
        "curr": "rub",
        "dest": -1257786,
        "nm": article
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


        data = response.json()


        products = (
            data
            .get("data", {})
            .get("products", [])
        )


        if not products:

            raise Exception(
                "Карточка WB не найдена"
            )


        product = products[0]


        price_data = (
            product
            .get("sizes", [{}])[0]
            .get("price", {})
        )


        price = (
            price_data
            .get("product", 0)
            // 100
        )


        old_price = (
            price_data
            .get("basic", 0)
            // 100
        )


        discount = 0

        if old_price:

            discount = round(
                (1 - price / old_price) * 100
            )


        image = (
            f"https://basket-01.wbbasket.ru/"
            f"vol{article//100000}/"
            f"part{article//1000}/"
            f"{article}/images/big/1.webp"
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
                    0
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


        return {

            "market": "🟣 Wildberries",

            "article": "ошибка",

            "name": f"Ошибка: {e}",

            "price": "0 ₽",

            "old_price": "0 ₽",

            "discount": "0%",

            "rating": "0",

            "reviews": "0",

            "link": "https://www.wildberries.ru",

            "image": None,

            "video": None
        }
