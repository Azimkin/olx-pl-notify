import sqlite3
from sqlite3 import Connection
from datetime import datetime

__DATABASE__: Connection


def connect(db_name: str = 'database'):
    global __DATABASE__
    __DATABASE__ = sqlite3.connect(db_name + ".db")
    print(f"Connected to {db_name}.db")
    initialize_database(__DATABASE__)


def initialize_database(conn: Connection):
    conn.execute('''
                 CREATE TABLE IF NOT EXISTS advertisements
                 (
                     id           INTEGER PRIMARY KEY AUTOINCREMENT,
                     platform_id  INTEGER  NOT NULL,
                     published_on DATETIME NOT NULL
                 )''')
    conn.execute('''
                 CREATE TABLE IF NOT EXISTS users
                 (
                     id         INTEGER PRIMARY KEY,
                     subscribed INTEGER NOT NULL
                 )''')


def check(id: int, publish_time: datetime) -> bool:
    res = __DATABASE__.execute('''SELECT *
                                  FROM advertisements
                                  WHERE platform_id = ?''', (id,))
    for i in res.fetchall():
        return True
    return False


def add(id: int, publish_time: datetime) -> int:
    res = __DATABASE__.execute('''INSERT INTO advertisements(platform_id, published_on)
                                  VALUES (?, ?)''', (id, publish_time))
    __DATABASE__.commit()
    return res.lastrowid


def remove(id: int | None = None, platform_id: int | None = None):
    ...


def is_subscriber(id: int) -> bool:
    res = __DATABASE__.execute('''SELECT *
                                  FROM users
                                  WHERE id = ?''', (id,)).fetchone()
    return res and res[1] > 0


def subscribe(id: int):
    __DATABASE__.execute('''INSERT INTO users(id, subscribed)
                            VALUES (?, ?)''', (id, 1))
    __DATABASE__.commit()


def unsubscribe(id: int):
    __DATABASE__.execute('''DELETE
                            FROM users
                            WHERE id = ?''', (id,))
    __DATABASE__.commit()


def get_subscribers() -> list[int]:
    res = __DATABASE__.execute('''SELECT * FROM users''')
    return list(i[0] for i in res.fetchall())