import psycopg2
from psycopg2 import Error
import random
import string
import logging
from fastapi import FastAPI

app = FastAPI()

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DB_CONFIG = {
    "user": "postgres",
    "password": "123",
    "host": "127.0.0.1",
    "port": "5432",
    "database": "cyberED"
}

def create_table():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        create_table_query = """
        CREATE SCHEMA IF NOT EXISTS common;
        CREATE TABLE IF NOT EXISTS common.passwords (
            id SERIAL PRIMARY KEY,
            password_value TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        logging.info("Таблица common.passwords успешно создана или уже существует.")
    except (Exception, Error) as error:
        logging.error(f"Ошибка при создании таблицы: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()

create_table()

def random_char(char_num):
    return ''.join(random.choice(string.ascii_letters) for _ in range(char_num))

def generate_email():
    return random_char(7).lower() + "@cybered.com"

@app.post("/add_password")
async def add_password():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        password_value = random_char(10)
        email = generate_email()
        postgres_insert_query = """INSERT INTO common.passwords (password_value, email) VALUES (%s, %s) RETURNING id;"""
        cursor.execute(postgres_insert_query, (password_value, email))
        password_id = cursor.fetchone()
        connection.commit()
        if password_id:
            logging.info(f"Добавлен новый пароль с ID {password_id[0]} и email {email}")
            return {"message": "Password added successfully", "id": password_id[0], "password": password_value, "email": email}
        else:
            logging.warning("ID не был возвращен при добавлении пароля.")
            return {"error": "ID не был возвращен"}
    except (Exception, Error) as error:
        logging.error(f"Ошибка при добавлении пароля: {error}")
        return {"error": str(error)}
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.get("/passwords")
async def read_passwords():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute("SELECT id, password_value, email FROM common.passwords")
        passwords = cursor.fetchall()
        logging.info("Получен список паролей и email из базы данных.")
        return {"passwords": passwords}
    except (Exception, Error) as error:
        logging.error(f"Ошибка при получении паролей: {error}")
        return {"error": str(error)}
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.get("/")
async def main():
    logging.info("API is running")
    return {"message": "API is running"}