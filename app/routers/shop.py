import base64
import math
import os
from app.models.model_user import User
import app.utils.util_file as UtilFile
from fastapi import APIRouter, File, UploadFile
import sqlite3
router = APIRouter()


@router.get('/getImg')
async def getImg():
    pathImage = os.path.realpath('./app/src/image')
    path = os.path.realpath(pathImage + '/food.jpg')
    if(os.path.exists(path)):
        with open(path, 'rb') as f:
            file = f.read()
            encoded = base64.b64encode(file)
            return {'file_name': os.path.basename(f.name), 'size': UtilFile.convert_size(f.seek(0, os.SEEK_END)), 'result': encoded}
    else:
        return {'error': 'file not found'}


# @router.post('/createUser')
# async def create_user(user: User):
#     print(user)
#     conn = sqlite3.connect("database.db")
#     query = "INSERT INTO Users (Name, User, Email, Password) VALUES ('{name}', '{user}', '{email}', '{password}')"
#     conn.execute(query.format(name = user.name, user = user.user, password = user.password, email = user.email))
#     conn.commit()
#     conn.close()

# @router.put('/updateUser')
# async def update_user(user: User):
#     print(user)
#     conn = sqlite3.connect("database.db")
#     query = "UPDATE Users SET Name='{name}', User = '{user}', Email= '{email}', Password = '{password}' WHERE id='{id}'"
#     conn.execute(query.format(id = user.id, name = user.name, user = user.user, email = user.email, password = user.password))
#     conn.commit()
#     conn.close()

# @router.delete("/deleteUser/{id}")
# async def delete_user(id: int):
#     print(id)
#     conn = sqlite3.connect("database.db")
#     query = "DELETE FROM Users WHERE id='{id}'"
#     conn.execute(query.format(id = id))
#     conn.commit()
#     conn.close()
