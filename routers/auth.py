from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from schemas.usuario import UsuarioCreate
from models.usuario import Usuario
from auth.hash import hash_password, verify_password
from auth.jwt import create_token, get_db



router = APIRouter(prefix ="/auth", tags=["auth"])

@router.post("/registro")
def registro(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email== usuario.email).first():
        raise HTTPException(status_code=400, detail="Usuario ya reisrado")
    nuevo_usuario = Usuario(email=usuario.email, hashed_password=hash_password(usuario.password))
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {"msg": "Usuario registrado"}

@router.post("/login")
def login(form_data:OAuth2PasswordRequestForm = Depends(), db: Session = Depends (get_db)):
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="credenciales incorrectas",
        headers={"WWW-Authenticate": "Bearer"}
    )
    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    if not usuario or not verify_password(form_data.password, usuario.hashed_password):
        raise credentials_exception

    access_token = create_token({"sub": usuario.email})
    return {"access_token": access_token, "token_type": "bearer"}

    