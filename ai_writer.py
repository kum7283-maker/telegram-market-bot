import os
import logging
import requests


OPENAI_KEY = os.getenv("OPENAI_API_KEY")


logging.basicConfig(
    level=logging.INFO
)


def generate_post(news):

    title = news.get(
        "title",
        "Новости Москвы"
    )

    text = news.get(
        "text",
        ""
    )

    link = news.get(
        "link",
        ""
    )


    # Если нет ключа OpenAI
    if not OPENAI_KEY:

        logging.warning(
            "OPENAI_API_KEY не найден, работаем без AI"
        )

        return f"""
🚨 <b>{title}</b>

📍 Москва

{text}

🔗 Подробнее:
{link}

#Москва #НовостиМосквы
""".strip()



    prompt = f"""
Ты редактор Telegram-канала новостей Москвы.

Сделай короткий пост.

Правила:
- придумай интересный заголовок
- добавь эмодзи
- не выдумывай факты
- текст до 700 символов
- стиль городского новостного канала

Новость:

{title}

{text}
"""


    try:

        response = requests.post(

            "https://api.openai.com/v1/chat/completions",

            headers={

                "Authorization":
                f"Bearer {OPENAI_KEY}",

                "Content-Type":
                "application/json"

            },

            json={

                "model":
                "gpt-4o-mini",

                "messages":[

                    {
                        "role":
                        "system",

                        "content":
                        "Ты профессиональный редактор новостей."
                    },

                    {
                        "role":
                        "user",

                        "content":
                        prompt
                    }

                ],

                "temperature":
                0.6

            },

            timeout=40

        )


        data = response.json()


        # Проверяем ответ OpenAI

        if "choices" not in data:

            logging.error(
                f"OpenAI ошибка: {data}"
            )


            return f"""
🚨 <b>{title}</b>

📍 Москва

{text}

🔗 Подробнее:
{link}

#Москва #НовостиМосквы
""".strip()



        result = (
            data["choices"][0]
            ["message"]
            ["content"]
            .strip()
        )



        return f"""
{result}


🔗 Источник:
{link}


#Москва #НовостиМосквы
""".strip()



    except Exception as e:


        logging.error(
            f"AI ERROR: {e}"
        )


        return f"""
🚨 <b>{title}</b>

📍 Москва

{text}

🔗 Подробнее:
{link}

#Москва #НовостиМосквы
""".strip()
