import sqlite3

connection = sqlite3.connect('mydata.db')

curser = connection.cursor()

create_users_table = "CREATE TABLE users ( \
    id int , username text, password text \
)"

create_items_table = "CREATE TABLE items ( \
    name text, price text \
)"

curser.execute(create_users_table)
curser.execute(create_items_table)

connection.close()