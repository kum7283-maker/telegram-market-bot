import sqlite3
import hashlib
import os


DB_NAME = "news.db"



def get_connection():

    return sqlite3.connect(
        DB_NAME
    )



def init_db():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            hash TEXT UNIQUE,

            text TEXT,

            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """
    )


    conn.commit()

    conn.close()




def create_hash(text):

    return hashlib.md5(
        text.encode("utf-8")
    ).hexdigest()




def is_post_exists(text):

    conn = get_connection()

    cursor = conn.cursor()


    h = create_hash(text)


    cursor.execute(
        """
        SELECT id 
        FROM posts
        WHERE hash = ?
        """,
        (h,)
    )


    result = cursor.fetchone()


    conn.close()


    return result is not None





def save_post(text):


    if is_post_exists(text):

        return False



    conn = get_connection()

    cursor = conn.cursor()


    h = create_hash(text)


    cursor.execute(
        """
        INSERT INTO posts(hash,text)
        VALUES(?,?)
        """,
        (
            h,
            text
        )
    )


    conn.commit()

    conn.close()


    return True
