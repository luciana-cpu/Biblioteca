from passlib.context import CryptContext
from datetime import UTC, datetime, timedelta
from typing import Annotated
from jose import jwt, JWTError
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import session
from models.usuario import Usuario

from database import SessionLocal


SECRET_KEY = "tu_clave_secreta"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_sheme = OAuth2PasswordBearer (tokenUrl = "auth/login")


def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta (minutes =30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode (to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

def get_db ():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_usuario(token: Annotated[str, Depends(oauth2_sheme)], db: session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="token invalido",
        headers ={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms =[ALGORITHM])
        email = payload.get ("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(Usuario).filter (Usuario.email == email).first ()
    if user is None:
        raise credentials_exception
    return user
