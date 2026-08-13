import requests
import random


CATEGORIES = [
    "дом",
    "электроника",
    "авто",
    "инструменты",
    "одежда"
]


def get_product():

    query = random.choice(CATEGORIES)


    url = "https://search.wb.ru/exactmatch/ru/male/v4/search"


    params = {
        "query": query,
        "resultset": "catalog",
        "page": 1,
        "sort": "popular"
    }


    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }


    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=15
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
        raise Exception("WB не вернул товары")


    product = random.choice(products)


    article = product["id"]


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
            (1 - price / old_price) * 100
        )


    # фото WB
    basket = product.get("basket")
    vol = product.get("vol")
    part = product.get("part")
    root = product.get("root")


    image = None

    if basket and vol and part and root:

        image = (
            f"https://basket-{basket}.wbbasket.ru/"
            f"vol{vol}/part{part}/"
            f"{root}/images/big/1.webp"
        )


    return {

        "market": "🟣 Wildberries",

        "article": str(article),

        "name": product.get(
            "name",
            "Товар"
        ),

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
