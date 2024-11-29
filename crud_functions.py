import sqlite3

def get_all_products():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()

    cursor.execute("SELECT title, description, price FROM Products")
    result = cursor.fetchall()
    connection.close()
    return result


def intiate_db():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()

    connection1 = sqlite3.connect("database.db")
    cursor1 = connection1.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL
        );
    ''')
    connection.commit()
    cursor1.execute('''
           CREATE TABLE IF NOT EXISTS Users(
           id INTEGER PRIMARY KEY,
           username TEXT NOT NULL,
           email TEXT NOT NULL,
           age INTEGER NOT NULL,
           balance INTEGER NOT NULL
           );
       ''')
    connection1.commit()
    connection.close()
    connection1.close()

def is_included(user):
    connection1 = sqlite3.connect("database.db")
    cursor1 = connection1.cursor()
    res = cursor1.execute("SELECT * FROM Users WHERE username =?", (user,))
    return res.fetchone()

def add_user(username, email, age):

    if is_included(username) is None or False:
        connection1 = sqlite3.connect("database.db")
        cursor1 = connection1.cursor()
        balance = 1000
        cursor1.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                        (username, email, age, balance))
        connection1.commit()
        connection1.close()

# def add_data():
#     price = 100
#     for i in range(1,11):
#         cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)", (f"Продукт-{i}",
#                                                                                              f"Описание-{i}", price))
#         price += 100
#     connection.commit()

intiate_db()
#add_data()


