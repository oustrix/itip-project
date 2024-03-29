from datetime import datetime, timedelta

from fastapi import (
    status,
    HTTPException, Depends
)
from fastapi.security import OAuth2PasswordBearer
from jose import (
    jwt,
    JWTError,
)
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy import exc
from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session
from ..models.auth import User, Token, UserCreate, UserRole
from ..settings import settings

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in')


def get_current_user(token: str = Depends(oauth_scheme)) -> User:
    return AuthService.validate(token)


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def validate(cls, token: str) -> User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={
                'WWW-Authenticate': 'Bearer'
            }
        )

        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            raise exception from None

        user_data = payload.get('user')

        try:
            user = User.model_validate(user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    def create_token(cls, user: tables.User) -> Token:
        user_data = User.model_validate(user)

        now = datetime.utcnow()

        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expiration),
            'sub': str(user_data.id),
            'user': user_data.model_dump()
        }

        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm
        )

        return Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_user(self, user_data: UserCreate) -> Token:
        user = tables.User(
            email=user_data.email,
            name=user_data.name,
            surname=user_data.surname,
            password_hash=self.hash_password(user_data.password),
            role=user_data.role,
            balance=0,
            pending_money=0
        )
        self.session.add(user)

        try:
            self.session.commit()
        except exc.IntegrityError as ie:
            if ('users_email_key' in ie.args[0]) and ('duplicate' in ie.args[0]):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='Duplicate email'
                )

        if user.role == UserRole.WORKER:
            created_user = (
                self.session
                .query(tables.User)
                .filter_by(
                    email=user.email
                )
                .first()
            )
            worker = tables.Worker(
                user_id=created_user.id
            )
            self.session.add(worker)
            self.session.commit()

        return self.create_token(user)

    def authenticate_user(self, username: str, password: str) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={
                'WWW-Authenticate': 'Bearer'
            }
        )

        user = (
            self.session
            .query(tables.User)
            .filter(tables.User.username == username)
            .first()
        )

        if not user:
            raise exception

        if not self.verify_password(password, user.password_hash):
            raise exception

        return self.create_token(user)