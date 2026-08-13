import random


def get_products():

    products = [
        {
            "market": "🟣 Wildberries",
            "name": "Органайзер для хранения вещей",
            "price": "899 ₽",
            "old_price": "1990 ₽",
            "discount": "55%",
            "rating": "4.9",
            "reviews": "8500",
            "link": "https://www.wildberries.ru/"
        },

        {
            "market": "🟡 Ozon",
            "name": "Беспроводные наушники",
            "price": "1290 ₽",
            "old_price": "2990 ₽",
            "discount": "57%",
            "rating": "4.8",
            "reviews": "12000",
            "link": "https://www.ozon.ru/"
        },

        {
            "market": "🟣 Wildberries",
            "name": "Умные часы",
            "price": "1990 ₽",
            "old_price": "3990 ₽",
            "discount": "50%",
            "rating": "4.7",
            "reviews": "5400",
            "link": "https://www.wildberries.ru/"
        },

        {
            "market": "🟡 Ozon",
            "name": "Портативная колонка",
            "price": "1590 ₽",
            "old_price": "2990 ₽",
            "discount": "47%",
            "rating": "4.9",
            "reviews": "9200",
            "link": "https://www.ozon.ru/"
        }
    ]


    return random.choice(products)
