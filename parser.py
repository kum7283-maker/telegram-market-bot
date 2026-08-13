import requests
import random


ARTICLES = [
    "183126859",
    "145774392",
    "219739888"
]


def get_product():

    article = random.choice(ARTICLES)

    url = f"https://card.wb.ru/cards/v2/detail"

    params = {
        "appType": 1,
        "curr": "rub",
        "dest": -1257786,
        "nm": article
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "*/*",
        "Accept-Language": "ru-RU,ru;q=0.9"
    }


    try:

        r = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=20
        )


        print("STATUS:", r.status_code)
        print("TEXT:", r.text[:300])


        if not r.text:

            raise Exception("WB вернул пустой ответ")


        if not r.text.startswith("{"):

            raise Exception(
                "WB вернул не JSON: " + r.text[:50]
            )


        data = r.json()


        products = (
            data
            .get("data", {})
            .get("products", [])
        )


        if not products:

            raise Exception(
                "Карточка не найдена"
            )


        p = products[0]


        return {

            "market": "🟣 Wildberries",

            "article": article,

            "name": p.get(
                "name",
                "Без названия"
            ),

            "price": "0 ₽",

            "old_price": "0 ₽",

            "discount": "0%",

            "rating": str(
                p.get("rating",0)
            ),

            "reviews": str(
                p.get("feedbacks",0)
            ),

            "link":
            f"https://www.wildberries.ru/catalog/{article}/detail.aspx",

            "image": None,

            "video": None
        }


    except Exception as e:

        print("ERROR:", e)

        return {

            "market": "🟣 Wildberries",

            "article": article,

            "name": f"Ошибка: {e}",

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
