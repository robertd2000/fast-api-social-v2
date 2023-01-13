from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from db import get_db
from schemas.auth import Token
from schemas.user import UserCreate, User
from repository.users import create_user_in_db, get_user_and_check_password

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register', response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_in_db(user=user, db=db)


@router.post('/login', response_model=Token, status_code=status.HTTP_200_OK)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return get_user_and_check_password(request=request, db=db)
