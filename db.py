import sqlite3
from pathlib import Path

DB_PATH = Path("bot.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_url TEXT UNIQUE,
                text TEXT NOT NULL,
                telegram_message_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def save_post(product_url: str, text: str, telegram_message_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO posts
            (product_url, text, telegram_message_id)
            VALUES (?, ?, ?)
            """,
            (product_url, text, telegram_message_id),
        )
        conn.commit()
