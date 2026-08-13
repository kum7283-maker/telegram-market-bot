import random

def generate_post(product):
    title = product.get("title", "Товар с Wildberries и Ozon")
    price = product.get("price", "999")
    old_price = product.get("old_price", "1999")
    link = product.get("link", "https://www.wildberries.ru")

    discount = 0
    try:
        discount = int((1 - int(price) / int(old_price)) * 100)
    except:
        pass

    texts = [
        "🔥 Нашли выгодную цену!",
        "😍 Товар дня!",
        "⚡ Отличная находка с маркетплейса!"
    ]

    return f"""
{random.choice(texts)}

🛍 {title}

💰 Цена сейчас: {price} ₽
📉 Старая цена: {old_price} ₽
🔥 Скидка: {discount}%

🛒 Купить:
{link}

#ozon #wildberries #находки #скидки
"""
