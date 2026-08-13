def generate_post(product):

    name = product["name"]
    price = product["price"]
    old = product["old_price"]
    discount = product["discount"]
    rating = product["rating"]
    reviews = product["reviews"]
    link = product["link"]
    market = product["market"]


    text = f"""

🔥 НАХОДКА ДНЯ

{market}

😍 {name}

💰 Было: {old}
🔥 Сейчас: {price}

📉 Скидка: {discount}

⭐ Рейтинг: {rating}
💬 Отзывов: {reviews}

🛒 Забрать находку:
{link}


#находки #скидки #ozon #wildberries

"""


    return text.strip()
