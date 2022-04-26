from http.client import HTTPException
import os
import string
import base64
import io
import sqlite3
from app.models.model_item import Item
from app.models.model_response import Response
from app.models.model_store import Store
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
from passlib.hash import bcrypt

router = APIRouter()
JWT_SECRET = 'myjwtsecret'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get('/items/getItems')
async def items(user: User = Depends(get_current_user)):
    if not user:
        return Response.createError(errorList=[Error(code=status.HTTP_401_UNAUTHORIZED, message='Invalid username or password')])

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    # Verify whether the user exists or not
    verifyQuery = "SELECT i.Id, i.Title, i.Description, i.Price, ty.Title as TypeName, iimg.Image " + \
        "FROM Item i " + \
        "INNER JOIN ItemType ty ON i.IdType == ty.Id " + \
        "INNER JOIN (SELECT iimg.IdItem, iimg.Image FROM ItemImage iimg WHERE iimg.IsPrimary == 1 GROUP BY iimg.IdItem) iimg ON i.Id == iimg.IdItem "
    cursor.execute(verifyQuery)
    records = cursor.fetchall()
    result = []
    columnNames = [str(column[0]).lower() for column in cursor.description]
    for record in records:
        # Here is converted dict to entity
        result.append(Item.parse_obj(dict(zip(columnNames, record))))
    return Response.create(value=result)


@router.get('/store/getStores')
async def items():
    # user: User = Depends(get_current_user)
    # if not user:
    #     return Response.createError(errorList=[Error(code=status.HTTP_401_UNAUTHORIZED, message='Invalid username or password')])

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    # Verify whether the user exists or not
    verifyQuery = "SELECT store.Id, store.Name, store.Description, storeImage.Image " + \
        "FROM Store store " + \
        "INNER JOIN (SELECT storeImage.IdStore, storeImage.Image FROM StoreImage storeImage GROUP BY storeImage.IdStore) storeImage ON store.Id == storeImage.IdStore "
    cursor.execute(verifyQuery)
    records = cursor.fetchall()
    result = []
    columnNames = [str(column[0]).lower() for column in cursor.description]
    for record in records:
        # Here is converted dict to entity
        result.append(Store.parse_obj(dict(zip(columnNames, record))))
    return Response.create(value=result)
