from settings import big_data_base
import sqlalchemy
import psycopg2
import sqlite3


def start_db():
    connect = sqlite3.connect('data_base_file.db')
    connection = connect.cursor()
    return connection


def create_db():
    connection = start_db()
    connection.execute("""CREATE TABLE IF NOT EXISTS vk_users(
                       id INTEGER PRIMARY KEY ,
                       popularity INTEGER ,
                       photo1 VARCHAR (300) ,
                       photo2 VARCHAR (300) ,
                       photo3 VARCHAR (300)
                       );
        """)
    return


def add_user(user):
    connect = sqlite3.connect('data_base_file.db')
    connection = connect.cursor()
    filler = ['0', '0', '0', '0', '0']
    filler[0] = user['id']
    filler[1] = user['pop']
    x = 2
    for photo_info in user['photo']:
        filler[x] = photo_info['url']
        x += 1
    filler = [(str(x, )) for x in filler]
    filler = tuple(filler)
    connection.execute("""INSERT INTO vk_users(id, popularity, photo1, photo2, photo3)
                           VALUES (?, ?, ?, ?, ? ); """, filler)
    connect.commit()
    connection.close()
    return


def get_id():
    connection = start_db()
    all_id = connection.execute("""SELECT id FROM vk_users""").fetchall()
    all_id = [list(x) for x in all_id]
    all_id = [int(x[0]) for x in all_id]
    return all_id


def clear_db():
    connect = sqlite3.connect('data_base_file.db')
    connection = connect.cursor()
    connection.execute("""DELETE FROM vk_users ;""")
    connect.commit()
    connection.close()
    return
