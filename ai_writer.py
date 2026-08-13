import os
from openai import AsyncOpenAI

SYSTEM_PROMPT = """
Ты — редактор Telegram-канала «WB × OZON НАХОДКИ».
Пиши короткие, живые и энергичные посты на русском.
Структура:
🔥 короткий заголовок
1–3 предложения с пользой товара
💰 цена и скидка
🛒 ссылка
2–4 релевантных хэштега

Не выдумывай характеристики, которых нет во входных данных.
Не используй длинные рекламные полотна.
"""

async def generate_post(product: dict) -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if not api_key:
        return (
            f"🔥 НАХОДКА ДНЯ\n\n"
            f"😍 {product['title']} — отличный вариант для дома!\n\n"
            f"💰 Было: {product['old_price']} ₽\n"
            f"🔥 Сейчас: {product['price']} ₽\n"
            f"📉 Скидка: {product['discount']}%\n\n"
            f"🛒 Забрать находку → {product['url']}\n\n"
            f"#находки #скидка #ozon #wb"
        )

    client = AsyncOpenAI(api_key=api_key)

    prompt = (
        f"Название: {product['title']}\n"
        f"Цена: {product['price']} ₽\n"
        f"Старая цена: {product['old_price']} ₽\n"
        f"Скидка: {product['discount']}%\n"
        f"Ссылка: {product['url']}\n"
    )

    response = await client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
        instructions=SYSTEM_PROMPT,
        input=prompt,
    )
    return response.output_text.strip()
