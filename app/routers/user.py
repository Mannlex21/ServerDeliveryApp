from app.models.model_user import User
from fastapi import APIRouter
import sqlite3
router = APIRouter()

@router.get('/getUsers')
async def get():
    conn = sqlite3.connect("database.db")
    cur = conn.execute("select*from Users")
    users = cur.fetchall()
    result_prueba = []
    for i in users:
        single_prueba = {}
        single_prueba["Id"] = i[0]
        single_prueba["Name"] = i[1]
        single_prueba["User"] = i[2]
        single_prueba["Email"] = i[3]
        single_prueba["Password"] = i[4]
        result_prueba.append(single_prueba)
    conn.commit()
    conn.close()
    return result_prueba

@router.post('/createUser')
async def create_user(user: User):
    print(user)
    conn = sqlite3.connect("database.db")
    query = "INSERT INTO Users (Name, User, Email, Password) VALUES ('{name}', '{user}', '{email}', '{password}')"
    conn.execute(query.format(name = user.name, user = user.user, password = user.password, email = user.email))
    conn.commit()
    conn.close()

@router.put('/updateUser')
async def update_user(user: User):
    print(user)
    conn = sqlite3.connect("database.db")
    query = "UPDATE Users SET Name='{name}', User = '{user}', Email= '{email}', Password = '{password}' WHERE id='{id}'"
    conn.execute(query.format(id = user.id, name = user.name, user = user.user, email = user.email, password = user.password))
    conn.commit()
    conn.close()

@router.delete("/deleteUser/{id}")
async def delete_user(id: int):
    print(id)
    conn = sqlite3.connect("database.db")
    query = "DELETE FROM Users WHERE id='{id}'"
    conn.execute(query.format(id = id))
    conn.commit()
    conn.close()