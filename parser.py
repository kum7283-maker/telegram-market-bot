import requests
import random


PRODUCTS = [
    123456789,
    987654321
]


def get_product():

    article = random.choice(PRODUCTS)

    url = (
        f"https://card.wb.ru/cards/v2/detail"
    )

    params = {
        "appType": 1,
        "curr": "rub",
        "dest": -1257786,
        "nm": article
    }


    headers = {
        "User-Agent": "Mozilla/5.0"
    }


    try:

        r = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=15
        )


        data = r.json()


        card = data["data"]["products"][0]


        name = card.get(
            "name",
            "Товар WB"
        )


        price = (
            card["sizes"][0]["price"]["product"]
            // 100
        )


        old_price = (
            card["sizes"][0]["price"]["basic"]
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

            "name": name,

            "price": f"{price} ₽",

            "old_price": f"{old_price} ₽",

            "discount": f"{discount}%",

            "rating": str(
                card.get("rating", "")
            ),

            "reviews": str(
                card.get("feedbacks", "")
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
            "article": "ошибка",
            "name": "Ошибка получения карточки",
            "price": "0 ₽",
            "old_price": "0 ₽",
            "discount": "0%",
            "rating": "0",
            "reviews": "0",
            "link": "https://www.wildberries.ru",
            "image": None,
            "video": None
        }
