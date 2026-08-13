def generate_post(product):

    title = product.get("title", "Интересный товар")
    price = product.get("price", "Нет цены")
    old_price = product.get("old_price", "")
    link = product.get("link", "")

    discount = ""

    try:
        if old_price and int(old_price) > int(price):
            discount = int((1 - int(price) / int(old_price)) * 100)
    except:
        pass

    text = f"""
🔥 НАХОДКА ДНЯ

🛒 {title}

💰 Цена: {price} ₽
"""

    if old_price:
        text += f"❌ Было: {old_price} ₽\n"

    if discount:
        text += f"📉 Скидка: {discount}%\n"

    text += f"""
🔗 Купить:
{link}

#wb #ozon #находки
"""

    return text
