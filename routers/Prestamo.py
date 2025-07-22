from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from models.libro import Libro
from models.Prestamo import Prestamo
from auth.jwt import get_db, get_current_usuario
import schemas


router = APIRouter(prefix = "/prestar", tags = ["prestar"])



@router.post("/prestar")
def prestar_libro(libro_id: int, db: Session = Depends(get_db), usuario=Depends(get_current_usuario)):
    lib = db.query(Libro).get(libro_id)
    if not lib or not lib.disponible:
        raise HTTPException(status_code=400, detail="Libro no disponible")
    lib.disponible = False
    prestamo = Prestamo(libro_id=lib.id, usuario_id=usuario.id)
    db.add(prestamo)
    db.commit()
    return {"msg": "Préstamo registrado"}

