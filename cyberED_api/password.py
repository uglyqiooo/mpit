import psycopg2
from psycopg2 import Error
import random
import string
from fastapi import FastAPI

app = FastAPI()

try:
    # Подключиться к существующей базе данных
    connection = psycopg2.connect(user="postgres",  # Проверьте имя пользователя
                                  password="123",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="cyberED")

    cursor = connection.cursor()

    postgres_insert_query = """INSERT INTO password (id, password) VALUES (%s, %s)"""
    record_to_insert = (5, 'OnePlus6_950')
    cursor.execute(postgres_insert_query, record_to_insert)

    connection.commit()
    count = cursor.rowcount
    print(count, "Запись успешно добавлена в таблицу passwords")

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL:", error)

finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")


def random_char(char_num):
    return ''.join(random.choice(string.ascii_letters) for _ in range(char_num))


print(random_char(7))


@app.get("/passwords")
async def read_users():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="123",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="cyberED")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM common.passwords")
        users = cursor.fetchall()
        return {"users": users}

    except (Exception, Error) as error:
        return {"error": str(error)}

    finally:
        if connection:
            cursor.close()
            connection.close()


@app.get("/")
async def main():
    return {"message": "lorem ipsum"}
