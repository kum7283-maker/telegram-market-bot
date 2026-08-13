import sqlite3


def init_db():

    con = sqlite3.connect("posts.db")

    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS posts(
        id INTEGER PRIMARY KEY,
        text TEXT
    )
    """)


    con.commit()
    con.close()



def save_post(text):

    con = sqlite3.connect("posts.db")

    cur = con.cursor()

    cur.execute(
        "INSERT INTO posts(text) VALUES(?)",
        (text,)
    )

    con.commit()
    con.close()
