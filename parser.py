import requests
import random


def get_wb_products():
    products = [
        {
            "name": "Беспроводные наушники",
            "price": "1290 ₽",
            "old_price": "2990 ₽",
            "discount": "-57%",
            "rating": "4.8",
            "link": "https://www.wildberries.ru/"
        },
        {
            "name": "Умные часы",
            "price": "1990 ₽",
            "old_price": "3990 ₽",
            "discount": "-50%",
            "rating": "4.7",
            "link": "https://www.wildberries.ru/"
        }
    ]

    return random.choice(products)



def get_ozon_products():
    products = [
        {
            "name": "Портативная колонка",
            "price": "1590 ₽",
            "old_price": "2990 ₽",
            "discount": "-47%",
            "rating": "4.9",
            "link": "https://www.ozon.ru/"
        },
        {
            "name": "Массажёр для спины",
            "price": "2490 ₽",
            "old_price": "4990 ₽",
            "discount": "-50%",
            "rating": "4.8",
            "link": "https://www.ozon.ru/"
        }
    ]

    return random.choice(products)



def get_random_product():

    if random.choice([True, False]):
        return get_wb_products()

    return get_ozon_products()
