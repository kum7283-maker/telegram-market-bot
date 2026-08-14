import os
import requests
import html


OPENAI_KEY = os.getenv("OPENAI_API_KEY")


def generate_post(news):

    title = news.get("title", "Новости Москвы")
    text = news.get("text", "")
    link = news.get("link", "")


    # очищаем для Telegram

    title = html.escape(title)
    text = html.escape(text)



    # Если нет ключа OpenAI

    if not OPENAI_KEY:

        return f"""
🚨 {title}

📍 Москва

{text}

🔗 Подробнее:
{link}

#Москва #НовостиМосквы
""".strip()



    try:

        prompt = f"""
Ты редактор Telegram-канала новостей Москвы.

Перепиши новость:
- коротко
- интересно
- без выдуманных фактов
- добавь 1-2 эмодзи

Заголовок:
{title}

Текст:
{text}
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

                "temperature": 0.5

            },

            timeout=40

        )


        data = response.json()


        # Проверка ответа OpenAI

        if "choices" not in data:

            print("OPENAI ERROR:", data)

            result = text


        else:

            result = data["choices"][0]["message"]["content"]



        result = html.escape(result)



        return f"""
{result}

🔗 Источник:
{link}

#Москва #НовостиМосквы
""".strip()



    except Exception as e:


        print("AI ERROR:", e)


        return f"""
🚨 {title}

📍 Москва

{text}

🔗 Подробнее:
{link}

#Москва #НовостиМосквы
""".strip()
