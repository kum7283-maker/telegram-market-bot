import random


def get_wb_products():
    """
    Временный модуль поиска товаров WB.
    Следующим этапом подключим реальный сбор данных.
    """

    products = [
        {
            "market": "Wildberries",
            "name": "Беспроводные наушники",
            "price": "1499 ₽",
            "old_price": "2999 ₽",
            "rating": "4.8",
            "reviews": "12500",
            "url": "https://www.wildberries.ru/",
            "category": "Электроника"
        },
        {
            "market": "Wildberries",
            "name": "Органайзер для дома",
            "price": "599 ₽",
            "old_price": "999 ₽",
            "rating": "4.9",
            "reviews": "8700",
            "url": "https://www.wildberries.ru/",
            "category": "Дом"
        }
    ]

    return random.choice(products)
