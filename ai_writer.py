def generate_post(news):


    title = news.get(
        "title",
        "Москва"
    )


    text = news.get(
        "text",
        ""
    )


    link = news.get(
        "link",
        ""
    )


    return f"""

🚨 <b>{title}</b>


📍 Москва


{text}


🔗 Подробнее:
{link}


#Москва #НовостиМосква

""".strip()
