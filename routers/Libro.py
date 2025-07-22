from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.libro import LibroCreate, LibroOut
from models.libro import Libro
from auth.jwt import get_db, get_current_usuario
from typing import List

router = APIRouter(prefix="/Libros", tags=["libros"])

@router.post("/", response_model=LibroOut)
def crear_libro(data: LibroCreate, db: Session= Depends(get_db), user:dict=Depends(get_current_usuario)):
    nuevo = Libro(**data.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.get("/libros", response_model=list[LibroOut])
def listar_libros(db: Session = Depends(get_db), user = Depends (get_current_usuario)):
    return db.query(Libro).all()


