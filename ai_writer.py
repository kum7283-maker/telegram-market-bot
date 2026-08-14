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


    return f"""
🚨 **{title}**


📍 Москва


{text}


🔗 Подробнее:
{link}


#Москва #НовостиМосква #МоскваСейчас
""".strip()
