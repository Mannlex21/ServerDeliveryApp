from http.client import HTTPException
import os
import random
import string
import base64
import io
import sqlite3
from typing import List
from app.models.model_response import Response
import app.utils.util_file as UtilFile
import jwt
from app.models.model_user import User
from app.models.model_user_details import UserDetails
from app.models.model_error import Error
from app.models.model_image import Image as ModelImage
from app.db.auth import authenticate_user, get_current_user
from PIL import Image
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()
JWT_SECRET = 'myjwtsecret'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get('/client/currentUser')
async def current_user(user: User = Depends(get_current_user)):
    if not user:
        return Response.createError(errorList=[Error(code=status.HTTP_401_UNAUTHORIZED, message='Invalid username or password')])
    return Response.create(value=user)


@router.post('/client/login')
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        return Response.createError(errorList=[Error(code=status.HTTP_401_UNAUTHORIZED, message='Invalid username or password')])
    token = jwt.encode(user.dict(), JWT_SECRET)
    return Response.create(value={'access_token': token, 'token_type': 'bearer', 'status_code': status.HTTP_200_OK})


@router.post('/client/signUp')
async def sign_up(user: User, user_details: UserDetails):
    errors: list[Error] = []
    conn = sqlite3.connect("database.db")
    # Verify whether the user exists or not
    verifyQuery = "SELECT * FROM Users WHERE (Username = '{username}' or Email = '{email}')"
    queryExec = conn.execute(verifyQuery.format(
        email=user.email, username=user.username, password=user.password))
    data = queryExec.fetchone()

    if(data != None):
        errors.append(Error(code=0, message='User already exists'))
        return Response.createError(errorList=errors)
    # the user is created here
    key = ''.join(random.choice(string.ascii_letters) for i in range(20))
    query = "INSERT INTO Users (Username, Email, Password, Key) VALUES ('{username}', '{email}', '{password}', '{key}')"
    responseUser = conn.execute(query.format(
        username=user.username, password=user.password, email=user.email, key=key))

    if(responseUser.rowcount > 0):
        # the user details is created here
        query = "INSERT INTO UserDetails (IdUser, FirstName, LastName, AreaCode, PhoneNumber) VALUES ('{id_user}', '{first_name}', '{last_name}', '{area_code}', '{phone_number}')"
        response_details = conn.execute(query.format(
            id_user=responseUser.lastrowid, first_name=user_details.firstName, last_name=user_details.lastName, area_code=user_details.areaCode, phone_number=user_details.phoneNumber))

        if(response_details.rowcount > 0):
            # the profile images folder is created here
            pathImage = os.path.realpath('./app/src')
            mode = 0o666
            path = os.path.join(pathImage, 'image/users/{username}-{key}/profile'.format(
                username=user.username, key=key))
            None if os.path.exists(path) else os.makedirs(path, mode)
        else:
            errors.append(Error(code=0, message='Cannot insert user detail'))
    else:
        errors.append(Error(code=0, message='Cannot insert user'))
    conn.commit()
    conn.close()
    return Response.create() if len(errors) == 0 else Response.createError(errorList=errors)


@router.post('/client/uploadProfileImage')
async def uploadProfileImage(image: ModelImage, user: User = Depends(get_current_user)):
    if not user:
        return Response.createError(errorList=[Error(code=status.HTTP_401_UNAUTHORIZED, message='Invalid username or password')])

    if(os.path.exists(os.path.realpath('./app/src/image/users/'))):
        pathImage = os.path.realpath(
            './app/src/image/users/{username}-{key}/profile/{filename}.{type}'.format(username=user.username, key=user.key, filename="image", type='jpeg'))
        imageDecode = base64.b64decode(image.imageBase64)
        img = Image.open(io.BytesIO(imageDecode))
        img.save(os.path.realpath(pathImage))
        return Response.create()
    return Response.createError(errorList=[Error(message="Directory doesn't exist")])


@router.get('/client/getProfileImage')
async def getProfileImage(user: User = Depends(get_current_user)):
    if not user:
        return Response.createError(errorList=[Error(code=status.HTTP_401_UNAUTHORIZED, message='Invalid username or password')])
    pathImage = os.path.realpath('./app/src/image/users/{username}-{key}/profile/{filename}.{type}'.format(
        username=user.username, key=user.key, filename="image", type='jpeg'))

    if(os.path.exists(pathImage)):
        with open(pathImage, 'rb') as f:
            file = f.read()
            encoded = base64.b64encode(file)
            return Response.create(value={'file_name': os.path.basename(f.name), 'size': UtilFile.convert_size(f.seek(0, os.SEEK_END)), 'img64': encoded})
    return Response.createError(errorList=[Error(message='File not found')])


@router.delete('/client/deteleProfileImage')
async def deteleProfileImage(user: User = Depends(get_current_user)):
    if not user:
        return Response.createError(errorList=[Error(code=status.HTTP_401_UNAUTHORIZED, message='Invalid username or password')])

    pathImage = os.path.realpath('./app/src/image/users/{username}-{key}/profile/{filename}.{type}'.format(
        username=user.username, key=user.key, filename="image", type='jpeg'))

    if(os.path.exists(pathImage) == False):
        return Response.createError(errorList=[Error(message='File not found')])
    os.remove(pathImage)
    return Response.create()
