# WB × OZON НАХОДКИ — версия 1.1

Это обновлённая стартовая версия бота.

## Что исправлено

- Добавлена настройка `PROXY_URL` в `.env`.
- Прокси применяется и к обычным запросам Telegram, и к `get_updates`.
- Увеличены сетевые таймауты, чтобы кратковременные задержки не приводили к слишком быстрому падению.
- `ADMIN_ID` проверяется с понятным сообщением об ошибке.
- `/status` показывает, включён ли прокси.
- Секреты не входят в архив.

В `python-telegram-bot` 22.8 прокси задаётся через `proxy()` и `get_updates_proxy()`. Для SOCKS5 требуется дополнительная установка зависимости через `python-telegram-bot[socks]`.

## Запуск на Windows

1. Распакуй архив.
2. Скопируй `.env.example` в `.env`.
3. Заполни `.env`:
   - `BOT_TOKEN`
   - `CHANNEL_ID`
   - `ADMIN_ID`
   - при наличии прокси — `PROXY_URL`
   - при подключении ИИ — `OPENAI_API_KEY`

4. Установи зависимости:

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

5. Запусти:

```bat
python bot.py
```

6. В Telegram отправь боту `/start`, затем `/status`.

## Прокси

Пока прокси у нас нет, оставь:

```env
PROXY_URL=
```

Когда появится рабочий HTTP-прокси:

```env
PROXY_URL=http://IP:PORT
```

Для SOCKS5:

```env
PROXY_URL=socks5://IP:PORT
```

Для SOCKS5 нужно установить:

```bat
pip install "python-telegram-bot[socks]==22.8"
```

## Важно

Не отправляй `BOT_TOKEN` и `OPENAI_API_KEY` в чат и не добавляй `.env` в ZIP/Git.

Текущий товар всё ещё демо. Следующий этап — подключение реальных товаров WB/OZON, изображений, фильтра скидок, защиты от повторов и партнёрских ссылок.
