import os
import requests


OPENAI_KEY = os.getenv("OPENAI_API_KEY")


def generate_post(news):

    title = news.get("title", "")
    text = news.get("text", "")
    link = news.get("link", "")


    # Если ключа нет — обычный пост

    if not OPENAI_KEY:

        return f"""
🚨 <b>{title}</b>

📍 Москва

{text}

🔗 Подробнее:
{link}

#Москва #НовостиМосквы
""".strip()



    try:

        prompt = f"""
Ты редактор Telegram-канала новостей Москвы.

Создай короткий новостной пост.

Правила:
- придумай интересный заголовок
- используй эмодзи
- не выдумывай факты
- пиши простым языком
- максимум 5-7 предложений

Новость:

Заголовок:
{title}

Текст:
{text}

Сделай готовый пост для Telegram.
"""


        response = requests.post(

            "https://api.openai.com/v1/chat/completions",

            headers={

                "Authorization": f"Bearer {OPENAI_KEY}",

                "Content-Type": "application/json"

            },

            json={

                "model": "gpt-4o-mini",

                "messages": [

                    {

                        "role": "user",

                        "content": prompt

                    }

                ],

                "temperature": 0.7

            },

            timeout=30

        )


        data = response.json()


        result = data["choices"][0]["message"]["content"]


        return f"""
{result}

🔗 Источник:
{link}

#Москва #НовостиМосквы
""".strip()



    except Exception as e:


        print("AI ERROR:", e)


        return f"""
🚨 <b>{title}</b>

📍 Москва

{text}

🔗 Подробнее:
{link}

#Москва #НовостиМосквы
""".strip()
