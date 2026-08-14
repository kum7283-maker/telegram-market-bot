import os
import logging
import requests


OPENROUTER_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)


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



    if not OPENROUTER_KEY:


        return f"""
🚨 <b>{title}</b>

📍 Москва

{text}

🔗 Подробнее:
{link}

#Москва #НовостиМосквы
""".strip()



    prompt = f"""

Ты редактор Telegram канала Москва News.

Переделай новость.

Правила:
- короткий интересный заголовок
- добавь эмодзи
- стиль городского новостного канала
- не придумывай факты
- до 500 символов


Новость:

{title}

{text}

"""



    try:


        response = requests.post(


            "https://openrouter.ai/api/v1/chat/completions",


            headers={

                "Authorization":
                f"Bearer {OPENROUTER_KEY}",

                "Content-Type":
                "application/json"

            },


            json={

                "model":
                "openrouter/free",


                "messages":[

                    {
                        "role":
                        "user",

                        "content":
                        prompt
                    }

                ],

                "temperature":
                0.7

            },


            timeout=60

        )



        data = response.json()



        if "choices" not in data:

            logging.error(
                data
            )

            raise Exception(
                "AI не вернул ответ"
            )



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
