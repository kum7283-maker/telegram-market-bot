def generate_post(news):


    return f"""

🚨 <b>{news['title']}</b>


📍 Москва


{news['text']}


🔗 Подробнее:
{news['link']}


#Москва #НовостиМосквы

""".strip()
