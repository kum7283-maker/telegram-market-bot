def generate_post(product):

    return f"""
🔥 НАХОДКА ДНЯ


{product['market']}


😍 {product['name']}


💰 Было: {product['old_price']}

🔥 Сейчас: {product['price']}


📉 Скидка: {product['discount']}


⭐ Рейтинг: {product['rating']}

💬 Отзывов: {product['reviews']}


🛒 Забрать находку:

{product['link']}


#находки #скидки #ozon #wildberries
""".strip()
