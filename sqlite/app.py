import sqlite3

connection = sqlite3.connect('mydata.db')

curser = connection.cursor()

create_users_table = "CREATE TABLE IF NOT EXISTS users ( \
    id INTEGER PRIMARY KEY , username text, password text \
)"

create_items_table = "CREATE TABLE IF NOT EXISTS items ( \
    name text, price real \
)"

curser.execute(create_users_table)
curser.execute(create_items_table)

connection.close()