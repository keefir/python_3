import sqlite3

exit(1) # защита от случайного запуска

connection = sqlite3.connect('users.db')


with open('scheme.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("insert into users (email, name, login, password) values (?, ?, ?, ?)",
            ('admin@yahoo.com', 'admin', 'caos_enjoyer', 'adminadmin')
            )

connection.commit()
connection.close()