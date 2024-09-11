from jose import JWTError, jwt
from datetime import datetime, timedelta

from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from DiplomFastAPI.app.secret_key import secret_key
from passlib.context import CryptContext
import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from DiplomFastAPI.app.schemas import CreateUser
from sqlalchemy.orm import Session
from DiplomFastAPI.app.backend.db_depends import get_db
from typing import Annotated, List
from DiplomFastAPI.app.models.user import User
from sqlalchemy import insert, select, update, delete
from slugify import slugify

templates = Jinja2Templates(directory="DiplomFastAPI/app/templates")

SECRET_KEY = key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


router = APIRouter(prefix="/user", tags=["user"])


@router.post('/login', response_class=HTMLResponse)
async def login(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    username: str = Form(...),
    password: str = Form(...)
):
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    return RedirectResponse(url=f"/user/profile/{user.username}", status_code=status.HTTP_302_FOUND)


@router.post('/register', response_class=HTMLResponse)
async def register_user(db: Annotated[Session, Depends(get_db)],
                        request: Request,
                        user: CreateUser = Depends(CreateUser.as_form)):
    db.execute(insert(User).values(
        username=user.username,
        password=get_password_hash(user.password),
        first_name=user.first_name,
        last_name=user.last_name,
        age=user.age,
        slug=slugify(user.username)
    ))
    db.commit()
    return RedirectResponse(url=f"/user/profile/{user.username}", status_code=status.HTTP_302_FOUND)


@router.get('/profile/{username}', response_class=HTMLResponse)
async def user_profile(request: Request, db: Annotated[Session, Depends(get_db)], username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return HTMLResponse("User not found", status_code=404)

    return templates.TemplateResponse("profile.html", {"request": request, "user": user})

