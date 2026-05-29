from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

DATABASE = "users.db"


# Создание базы данных
def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


create_database()


# Модель пользователя
class UserCreate(BaseModel):
    username: str
    email: str


# Получить всех пользователей
@app.get("/users")
def get_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    conn.close()

    result = []

    for user in users:
        result.append({
            "id": user[0],
            "username": user[1],
            "email": user[2]
        })

    return result


# Получить пользователя по ID
@app.get("/users/{user_id}")
def get_user(user_id: int):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    conn.close()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user[0],
        "username": user[1],
        "email": user[2]
    }


# Создать пользователя
@app.post("/create_user")
def create_user(user: UserCreate):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        (user.username, user.email)
    )

    conn.commit()

    user_id = cursor.lastrowid

    conn.close()

    return {
        "message": "User created",
        "user": {
            "id": user_id,
            "username": user.username,
            "email": user.email
        }
    }

