import sqlite3, random


def new_user(tel_id, gender, status = 'normal'):
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        cursor.execute("INSERT INTO users VALUES (null,?,?,?)",(tel_id,gender,status,))

        connection.commit()
        return True
    except sqlite3.Error as error:
        print(error)
        return False
    finally:
        if connection:
            connection.close()



def new_female_advertisement(data):
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        # for save in data:
        #     res = data[save]
        #     exec(save + f"= '{res}'")
        # cursor.execute("SELECT user_id FROM users WHERE tel_id = (?)", (data['tel_id'],))
        # res = cursor.fetchone()
        # data['code_id'] = res[0]
        cursor.execute("INSERT INTO 'female-advertisement' VALUES (null,?,?,?,?,?,?,?,?,?,?,?)",(data['tel_id'],data['name'],data['age'],data['city'],data['height'],data['weight'],data['price'],data['number'],data['context'],data['code_id'],data['status']))

        connection.commit()
        return True
    except sqlite3.Error as error:
        print(error)
        return False
    finally:
        if connection:
            connection.close()


def new_save_code(code, tel_id):
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        
        cursor.execute('insert into "favorite" VALUES (?,?, "normal")', (tel_id,code,))
        connection.commit()

        return True
    except sqlite3.Error as error:
        print(error)
        return False
    finally:
        if connection:
            connection.close()


# def get_all_users():
#     connection = sqlite3.connect('database.db')
#     cursor = connection.cursor()

#     cursor.execute("SELECT * FROM users")

#     results = cursor.fetchall()

#     connection.commit()
#     connection.close()

#     return results


def get_id(tel_id):
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        # for save in data:
        #     res = data[save]
        #     exec(save + f"= '{res}'")
        cursor.execute("SELECT user_id FROM users WHERE tel_id = (?)", (tel_id,))
        res = cursor.fetchone()[0]
        return res
    except sqlite3.Error as error:
        print(error)
        return False
    finally:
        if connection:
            connection.close()


def get_all_advertisements(gender):
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        if gender == 'female':
            cursor.execute("SELECT code_id FROM 'female-advertisement'")
        elif gender == 'male':
            cursor.execute("SELECT * FROM 'male-advertisement'")

        results = cursor.fetchall()

        connection.commit()

        return results

    except sqlite3.Error as error:
        print(error) 
        return False
    finally:
        if connection:
            connection.close()


def get_code(code):
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM 'female-advertisement' WHERE code_id = (?)", (code,))

        result = cursor.fetchone()
        print(result)

        connection.commit()

        return result

    except sqlite3.Error as error:
        print(error) 
        return False
    finally:
        if connection:
            connection.close()


def get_saved_codes(tel_id):
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        
        cursor.execute("SELECT code_id FROM 'favorite' WHERE tel_id = (?)", (tel_id,))
        results = cursor.fetchall()
        
        connection.commit()

        return results

    except sqlite3.Error as error:
        print(error) 
        return False
    finally:
        if connection:
            connection.close()


def get_by_age(age):
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        age = int(age)
        if age == 1:
           cursor.execute("SELECT code_id FROM 'female-advertisement' WHERE age >= 18 and age <=29")
           results = cursor.fetchall()
        elif age == 2:
            cursor.execute("SELECT code_id FROM 'female-advertisement' WHERE age >= 30 and age <=39")
            results = cursor.fetchall()
        elif age == 3:
            cursor.execute("SELECT code_id FROM 'female-advertisement' WHERE age >= 40 and age <=49")
            results = cursor.fetchall()
        elif age == 4:
            cursor.execute("SELECT code_id FROM 'female-advertisement' WHERE age >= 50")
            results = cursor.fetchall()

        
        
        connection.commit()

        return results

    except sqlite3.Error as error:
        print(error) 
        return False
    finally:
        if connection:
            connection.close()



def get_by_price(price):
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        price = int(price)
        if price == 1:
            cursor.execute("SELECT code_id FROM 'female-advertisement' WHERE price <= 1000")
            results = cursor.fetchall()
        elif price == 2:
            cursor.execute("SELECT code_id FROM 'female-advertisement' WHERE price > 1000 and price <= 1500")
            results = cursor.fetchall()
        elif price == 3:
            cursor.execute("SELECT code_id FROM 'female-advertisement' WHERE price > 1500 and price <= 2000")
            results = cursor.fetchall()
        elif price == 4:
            cursor.execute("SELECT code_id FROM 'female-advertisement' WHERE price > 2000")
            results = cursor.fetchall()
        
        connection.commit()

        return results

    except sqlite3.Error as error:
        print(error) 
        return False
    finally:
        if connection:
            connection.close()




def check_user(tel_id):
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT tel_id FROM users WHERE tel_id = (?)",(tel_id,))
        exists = cursor.fetchone()
        connection.commit()
        if exists:
            return True
        return False
    except sqlite3.Error as error:
        print(error)
    finally:
        if connection:
            connection.close()


def check_female_advertisement(tel_id):
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT tel_id FROM 'female-advertisement' WHERE tel_id = (?)",(tel_id,))
        exists = cursor.fetchone()
        connection.commit()
        if exists:
            return True
        return False
    except sqlite3.Error as error:
        print(error)
    finally:
        if connection:
            connection.close()


def get_gender(tel_id):
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT gender FROM users WHERE tel_id = (?)",(tel_id,))
        gender = cursor.fetchone()
        connection.commit()
        return gender
    except sqlite3.Error as error:
        print(error)
        return False
    finally:
        if connection:
            connection.close()


def get_btn(code_id):
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT code_id,city,age FROM 'female-advertisement' WHERE code_id = (?)",(code_id,))
        res = cursor.fetchall()
        connection.commit()
        return res
    except sqlite3.Error as error:
        print(error)
        return False
    finally:
        if connection:
            connection.close()

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

# cursor.execute("DROP TABLE advertisements")

# cursor.execute("""
#     CREATE TABLE advertisements (
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

# cursor.execute("INSERT INTO advertisements VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",(user_id,gender,name,age,city,height,weight,price,number,context,photo,code))

# data = {'tel_id': 1020718360, 'name': 'فلان فلانی', 'age': '30', 'city': 'تهران', 'height': '170', 'weight': '70', 'price': '800', 'number': '09652398741', 'context': 'سلام خوبین من خوبم دیگه چه خبر'}

