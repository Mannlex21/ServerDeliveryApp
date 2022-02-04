from http.client import HTTPException
import os
import random
import string
import base64
import io
import sqlite3
import app.utils.util_file as UtilFile
import jwt
from app.models.model_login import Login
from app.models.model_user import User
from app.models.model_image import Image as ModelImage
from app.models.model_login import Login
from PIL import Image
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt

router = APIRouter()
JWT_SECRET = 'myjwtsecret'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await get_user(id=payload.get('id'))
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid username or password')
    return user


async def authenticate_user(username: str, password: str):
    conn = sqlite3.connect("database.db")
    query = "SELECT * FROM Users WHERE (Username = '{emailOrUser}' or Email = '{emailOrUser}') and Password = '{password}'"
    login = conn.execute(query.format(
        emailOrUser=username, password=password))
    result = login.fetchone()
    conn.commit()
    conn.close()
    return None if result == None else User(id=result[0], username=result[1], email=result[2], password=bcrypt.hash(result[3]))


async def get_user(id):
    conn = sqlite3.connect("database.db")
    query = "SELECT * FROM Users WHERE Id = '{id}'"
    login = conn.execute(query.format(id=id))
    result = login.fetchone()
    conn.commit()
    conn.close()
    return None if result == None else User(id=result[0], username=result[1], email=result[2], password=bcrypt.hash(result[3]))


@router.get('/users/me', response_model=User)
async def index(user: User = Depends(get_current_user)):
    return user


@router.post('/token')
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data)
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid username or password')
    token = jwt.encode(user.dict(), JWT_SECRET)
    return {'access_token': token, 'token_type': 'bearer', 'status_code': status.HTTP_200_OK}


@router.post('/client/signUp')
async def sign_up(user: User):
    print(user)
    valueResult = False
    conn = sqlite3.connect("database.db")
    # Verify whether the user exists or not
    verifyQuery = "SELECT * FROM Users WHERE (Username = '{username}' or Email = '{email}') and Password = '{password}'"
    queryExec = conn.execute(verifyQuery.format(
        email=user.email, username=user.username, password=user.password))
    data = queryExec.fetchone()

    # Here is created the user
    if(data == None):
        key = ''.join(random.choice(string.ascii_letters) for i in range(20))
        query = "INSERT INTO Users (Username, Email, Password, Key) VALUES ('{username}', '{email}', '{password}', '{key}')"
        signUp = conn.execute(query.format(
            username=user.username, password=user.password, email=user.email, key=key))
        valueResult = True if signUp.rowcount > 0 else False

        # Here is created the profile images folder
        if(valueResult == True):
            pathImage = os.path.realpath('./app/src')
            mode = 0o666
            path = os.path.join(pathImage, 'image/users/{username}-{key}/profile'.format(
                username=user.username, key=key))
            None if os.path.exists(path) else os.makedirs(path, mode)
    conn.commit()
    conn.close()
    return valueResult


@router.post('/client/uploadProfileImage')
async def uploadProfileImage(login: Login, image: ModelImage):
    conn = sqlite3.connect("database.db")
    query = "SELECT * FROM Users WHERE (Username = '{emailOrUser}' or Email = '{emailOrUser}') and Password = '{password}'"
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
    query = "SELECT * FROM Users WHERE (Username = '{emailOrUser}' or Email = '{emailOrUser}') and Password = '{password}'"
    login = conn.execute(query.format(
        emailOrUser=login.emailOrUser, password=login.password))
    result = login.fetchone()
    if(result != None):
        print(result)
        pathImage = os.path.realpath('./app/src/image/users/{username}-{key}/profile/{filename}.{type}'.format(
            username=result[1], key=result[4], filename="image", type='jpeg'))

        if(os.path.exists(pathImage)):
            with open(pathImage, 'rb') as f:
                file = f.read()
                encoded = base64.b64encode(file)
                return {'failed': False, 'success': True, 'file_name': os.path.basename(f.name), 'size': UtilFile.convert_size(f.seek(0, os.SEEK_END)), 'result': encoded}
    else:
        return {'status_code': status.HTTP_200_OK, 'success': False, 'detail': 'user not found'}


@router.post('/client/deteleProfileImage')
async def deteleProfileImage(login: Login):
    conn = sqlite3.connect("database.db")
    query = "SELECT * FROM Users WHERE (Username = '{emailOrUser}' or Email = '{emailOrUser}') and Password = '{password}'"
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
