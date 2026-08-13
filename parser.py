import random


def get_product():

    products = [

        {
            "market": "🟣 Wildberries",
            "name": "Робот-пылесос Xiaomi",
            "price": "8990 ₽",
            "old_price": "12990 ₽",
            "discount": "31%",
            "rating": "4.8",
            "reviews": "15000",
            "link": "https://www.wildberries.ru"
        },


        {
            "market": "🟡 Ozon",
            "name": "Беспроводные наушники Bluetooth",
            "price": "1290 ₽",
            "old_price": "2990 ₽",
            "discount": "57%",
            "rating": "4.9",
            "reviews": "12000",
            "link": "https://www.ozon.ru"
        },


        {
            "market": "🟣 Wildberries",
            "name": "Умные часы Smart Watch",
            "price": "1990 ₽",
            "old_price": "3990 ₽",
            "discount": "50%",
            "rating": "4.7",
            "reviews": "5400",
            "link": "https://www.wildberries.ru"
        },


        {
            "market": "🟡 Ozon",
            "name": "Органайзер для кухни",
            "price": "690 ₽",
            "old_price": "1490 ₽",
            "discount": "54%",
            "rating": "4.8",
            "reviews": "8700",
            "link": "https://www.ozon.ru"
        }

    ]


    return random.choice(products)
