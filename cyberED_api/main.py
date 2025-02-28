import uuid

import psycopg2
from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi import APIRouter
from psycopg2.extras import RealDictCursor
from sqlalchemy import select
from fastapi import FastAPI

from hashlib import sha1

sha = sha1(b'Hello Python').hexdigest()

print(sha)  # '422fbfbc67fe17c86642c5eaaa48f8b670cbed1b'





'''conn = psycopg2.connect(
    database="cyberED",
    user="postgresql",
    password="123",
    host="127.0.0.1",
    port="5432",
    cursor_factory=RealDictCursor)'''

conn = psycopg2.connect("dbname=cyberED user=postgres password=123 host=127.0.0.1 port=5432")

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
conn.set_client_encoding("UNICODE")
cur = conn.cursor()
app = FastAPI()

@app.get("/users")
async def read_users():
    cur.execute("SELECT * FROM common.employers")
    users = cur.fetchall()
    return {"users": users}




@app.get("/")
async def main():
    return "lorem ipsum"





