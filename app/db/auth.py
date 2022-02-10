import sqlite3
from app.models.model_user import User
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
import jwt

from app.models.model_user_details import UserDetails

JWT_SECRET = 'myjwtsecret'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authenticate_user(username: str, password: str):
    conn = sqlite3.connect("database.db")
    query = "SELECT * FROM Users WHERE Username = '{username}' and Password = '{password}'"
    login = conn.execute(query.format(
        username=username, password=password))
    result = login.fetchone()
    conn.commit()
    conn.close()
    return None if result == None else User(id=result[0], username=result[1], email=result[2], password=bcrypt.hash(result[3]), key=result[4])


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await get_user_by_id(id=payload.get('id'))
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid username or password')
    return None if user == None else user


async def get_user_by_id(id):
    conn = sqlite3.connect("database.db")
    query = "SELECT * FROM Users usr INNER JOIN USERDETAILS usrdetail ON usrdetail.IdUser == usr.Id WHERE Id = '{id}'"
    login = conn.execute(query.format(id=id))
    result = login.fetchone()
    conn.commit()
    conn.close()
    if(result == None):
        return None
    else:
        return User(
            id=result[0],
            username=result[1],
            email=result[2],
            key=result[4],
            details=UserDetails(
                firstName=result[7],
                lastName=result[8],
                areaCode=result[9],
                phoneNumber=result[10]
            )
        )
