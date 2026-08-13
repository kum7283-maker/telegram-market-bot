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


        # выбираем товар
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


        if old_price and price:

            discount = round(
                (1 - price / old_price) * 100
            )

        else:

            discount = 0



        # ссылка товара

        link = (
            f"https://www.wildberries.ru/catalog/"
            f"{article}/detail.aspx"
        )



        # данные для картинки

        vol = article // 100000

        part = article // 1000


        basket = product.get(
            "basket",
            "01"
        )


        image = (
            f"https://basket-{basket}.wbbasket.ru/"
            f"vol{vol}/part{part}/"
            f"{article}/images/big/1.webp"
        )



        # видео WB часто отсутствует

        video = None



        return {


            "market":
            "🟣 Wildberries",


            "article":
            str(article),


            "name":
            name,


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
                    "Нет"
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
            link,


            "image":
            image,


            "video":
            video

        }



    except Exception as e:


        print(
            "PARSER ERROR:",
            e
        )


        return {


            "market":
            "🟣 Wildberries",


            "article":
            "нет",


            "name":
            "Популярный товар",


            "price":
            "999 ₽",


            "old_price":
            "1999 ₽",


            "discount":
            "50%",


            "rating":
            "4.8",


            "reviews":
            "5000",


            "link":
            "https://www.wildberries.ru",


            "image":
            None,


            "video":
            None

        }
