import os
import logging

from openai import OpenAI


client = None


api_key = os.getenv(
    "OPENAI_API_KEY"
)


if api_key:

    client = OpenAI(
        api_key=api_key
    )



def local_rewrite(title, text):

    """
    Резерв без ИИ,
    если нет API ключа
    """

    text = text.replace(
        title,
        ""
    ).strip()


    if len(text) > 500:

        text = text[:500] + "..."


    return text





def generate_post(news):


    title = news.get(
        "title",
        "Новости Москвы"
    )


    description = news.get(
        "text",
        ""
    )


    link = news.get(
        "link",
        ""
    )



    # если есть GPT

    if client:


        try:


            response = client.chat.completions.create(

                model="gpt-4.1-mini",

                messages=[

                    {
                        "role": "system",

                        "content":
                        """
Ты редактор новостного Telegram-канала Москвы.

Задача:
- перепиши новость коротко;
- сохрани только факты;
- не придумывай детали;
- убери повтор заголовка;
- стиль: современный новостной канал.
Длина 2-4 предложения.
"""
                    },


                    {
                        "role": "user",

                        "content":
                        f"""
Заголовок:
{title}

Текст:
{description}
"""
                    }

                ],

                temperature=0.3

            )


            description = (

                response
                .choices[0]
                .message
                .content
                .strip()

            )


        except Exception as e:


            logging.error(
                f"AI ошибка: {e}"
            )


            description = local_rewrite(
                title,
                description
            )


    else:


        description = local_rewrite(
            title,
            description
        )




    # категория


    full = (
        title +
        " " +
        description
    ).lower()



    if any(
        x in full
        for x in [
            "полиция",
            "дтп",
            "напал",
            "нож",
            "задерж"
        ]
    ):

        category = (
            "🚨 ПРОИСШЕСТВИЯ",
            "#Происшествия"
        )


    elif any(
        x in full
        for x in [
            "метро",
            "автобус",
            "дорог"
        ]
    ):

        category = (
            "🚇 ТРАНСПОРТ",
            "#Транспорт"
        )


    else:

        category = (
            "📰 НОВОСТИ МОСКВЫ",
            "#Новости"
        )




    return f"""
{category[0]}


🚨 {title}


📍 Москва


{description}


🔗 Подробнее:
{link}


{category[1]} #Москва
""".strip()
