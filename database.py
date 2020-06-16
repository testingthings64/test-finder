import sqlite3


def new_user(tel_id, gender, status = 'normal'):
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO users VALUES (?,?,?)",(tel_id,gender,status))

    connection.commit()
    connection.close()

    return True


def new_advertisment(user_id,gender,name,age,city,height,weight,price,number,context,photo,code,status):
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO advertisments VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",(user_id,gender,name,age,city,height,weight,price,number,context,photo,code,status))

    connection.commit()
    connection.close()


def get_all_users():
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users")

    results = cursor.fetchall()

    connection.commit()
    connection.close()

    return results


def get_all_advertisments(gender):
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM advertisments WHERE gender = (?)",(gender,))

    results = cursor.fetchall()

    connection.commit()
    connection.close()

    return results


def check_user(tel_id):
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()

    cursor.execute("SELECT tel_id FROM users WHERE tel_id = (?)",(tel_id,))
    exists = cursor.fetchone()
    connection.commit()
    connection.close()
    if exists:
        return True
    return False


def get_gender(tel_id):
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()
    cursor.execute("SELECT gender FROM users WHERE tel_id = (?)",(tel_id,))
    gender = cursor.fetchone()
    connection.commit()
    connection.close()
    return gender

# cursor.execute(""" 
#     CREATE TABLE users (
#         tel_id integer PRIMARY KEY,
#         gender text,
#         status text
#     )
# """)

# many_users = [
#     (1234567890,'female','normal'),
#     (1234561234,'male','normal'),
#     (1234512340,'female','special'),
#     (1234123490,'female','special'),
# ]

# cursor.executemany("INSERT INTO users VALUES (?,?,?)",many_users)

# cursor.execute("DROP TABLE advertisments")

# cursor.execute("""
#     CREATE TABLE advertisments (
#         user_id integer,
#         gender text,
#         name text,
#         age integer,
#         city text,
#         height real,
#         weight real,
#         price integer,
#         number text,
#         context text,
#         photo blob,
#         code integer
#     )
# """)

# user_id = 1234512340
# gender = 'female'
# name = 'سارا خدایی'
# age = 25
# city = 'تهران'
# height = 166
# weight = 60
# price = 1800
# number = '09908562147'
# context = 'سلام من سارا هستم 25 ساله از تهران، حالمم خوبه'
# code = 1234567
# photo = None

# cursor.execute("INSERT INTO advertisments VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",(user_id,gender,name,age,city,height,weight,price,number,context,photo,code))
