def get_category(text):

    text = text.lower()


    if any(word in text for word in [
        "дтп",
        "полиция",
        "напал",
        "нож",
        "убил",
        "задерж",
        "преступ"
    ]):
        return (
            "🚨 ПРОИСШЕСТВИЯ",
            "#Происшествия"
        )


    if any(word in text for word in [
        "метро",
        "автобус",
        "трамвай",
        "мцд",
        "мцк",
        "дорог",
        "пробк"
    ]):
        return (
            "🚇 ТРАНСПОРТ",
            "#Транспорт"
        )


    if any(word in text for word in [
        "дожд",
        "снег",
        "погод",
        "мороз",
        "жара"
    ]):
        return (
            "🌧 ПОГОДА",
            "#Погода"
        )


    if any(word in text for word in [
        "стро",
        "дом",
        "жк",
        "ремонт"
    ]):
        return (
            "🏙 ГОРОД",
            "#Город"
        )


    return (
        "📰 ГЛАВНОЕ",
        "#Новости"
    )




def clean_description(text):

    text = text.replace(
        "\n",
        " "
    )

    text = text.strip()


    return text[:500]





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


    category, tag = get_category(
        title + " " + description
    )


    description = clean_description(
        description
    )


    return f"""
{category}


🚨 <b>{title}</b>


📍 Москва


{description}


🔗 Подробнее:
{link}


#{tag.replace("#","")} #Москва
""".strip()
