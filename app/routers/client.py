import os
import random
import re
import string
import base64
import io
import app.utils.util_file as UtilFile
from app.models.model_login import Login
from app.models.model_user import User
from app.models.model_image import Image as ModelImage
from app.models.model_login import Login
from PIL import Image
from fastapi import APIRouter
import sqlite3
router = APIRouter()


@router.post('/client/signIn')
async def sign_in(login: Login):
    print(login)
    conn = sqlite3.connect("database.db")
    query = "SELECT * FROM Users WHERE (User = '{emailOrUser}' or Email = '{emailOrUser}') and Password = '{password}'"
    login = conn.execute(query.format(
        emailOrUser=login.emailOrUser, password=login.password))
    result = login.fetchone()
    conn.commit()
    conn.close()
    return False if result == None else True


@router.post('/client/signUp')
async def sign_up(user: User):
    print(user)
    valueResult = False
    conn = sqlite3.connect("database.db")
    # Verify whether the user exists or not
    verifyQuery = "SELECT * FROM Users WHERE (User = '{user}' or Email = '{email}') and Password = '{password}'"
    queryExec = conn.execute(verifyQuery.format(
        email=user.email, user=user.user.lower(), password=user.password))
    data = queryExec.fetchone()

    # Here is created the user
    if(data == None):
        key = ''.join(random.choice(string.ascii_letters) for i in range(20))
        query = "INSERT INTO Users (User, Email, Password, Key) VALUES ('{user}', '{email}', '{password}', '{key}')"
        signUp = conn.execute(query.format(
            user=user.user.lower(), password=user.password, email=user.email, key=key))
        valueResult = True if signUp.rowcount > 0 else False

        # Here is created the profile images folder
        if(valueResult == True):
            pathImage = os.path.realpath('./app/src')
            mode = 0o666
            path = os.path.join(pathImage, 'image/users/{username}-{key}/profile'.format(
                username=user.user, key=key))
            None if os.path.exists(path) else os.makedirs(path, mode)
    conn.commit()
    conn.close()
    return valueResult


@router.post('/client/uploadProfileImage')
async def uploadProfileImage(login: Login, image: ModelImage):
    conn = sqlite3.connect("database.db")
    query = "SELECT * FROM Users WHERE (User = '{emailOrUser}' or Email = '{emailOrUser}') and Password = '{password}'"
    login = conn.execute(query.format(
        emailOrUser=login.emailOrUser, password=login.password))
    result = login.fetchone()
    if(result != None):
        pathImage = os.path.realpath(
            './app/src/image/users/{username}-{key}/profile/{filename}.{type}'.format(username=result[1], key=result[4], filename="image", type='jpeg'))
        imageDecode = base64.b64decode(image.imageBase64)
        img = Image.open(io.BytesIO(imageDecode))
        img.save(os.path.realpath(pathImage))
        return {'failed': False, 'success': True}
    return {'failed': True, 'success': False, 'error': 'file not found'}


@router.post('/client/getProfileImage')
async def getProfileImage(login: Login):
    conn = sqlite3.connect("database.db")
    query = "SELECT * FROM Users WHERE (User = '{emailOrUser}' or Email = '{emailOrUser}') and Password = '{password}'"
    login = conn.execute(query.format(
        emailOrUser=login.emailOrUser, password=login.password))
    result = login.fetchone()

    pathImage = os.path.realpath('./app/src/image/users/{username}-{key}/profile/{filename}.{type}'.format(
        username=result[1], key=result[4], filename="image", type='jpeg'))

    if(os.path.exists(pathImage)):
        with open(pathImage, 'rb') as f:
            file = f.read()
            encoded = base64.b64encode(file)
            return {'failed': False, 'success': True, 'file_name': os.path.basename(f.name), 'size': UtilFile.convert_size(f.seek(0, os.SEEK_END)), 'result': encoded}
    else:
        return {'failed': True, 'success': False, 'error': 'file not found'}


@router.post('/client/deteleProfileImage')
async def deteleProfileImage(login: Login):
    conn = sqlite3.connect("database.db")
    query = "SELECT * FROM Users WHERE (User = '{emailOrUser}' or Email = '{emailOrUser}') and Password = '{password}'"
    login = conn.execute(query.format(
        emailOrUser=login.emailOrUser, password=login.password))
    result = login.fetchone()

    pathImage = os.path.realpath('./app/src/image/users/{username}-{key}/profile/{filename}.{type}'.format(
        username=result[1], key=result[4], filename="image", type='jpeg'))

    if(os.path.exists(pathImage)):
        os.remove(pathImage)
        return {'failed': False, 'success': True}
    else:
        return {'failed': True, 'success': False, 'error': 'file not found'}
