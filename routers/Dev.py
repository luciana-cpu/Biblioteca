from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.Prestamo import Prestamo
from models.libro import Libro
from auth.jwt import get_db, get_current_usuario
import schemas


router = APIRouter(prefix= "/devolver", tags=["devolver"])


@router.post("/devolver/{id}")
def devolver_libro(id: int, db: Session = Depends(get_db), usuario=Depends(get_current_usuario)):
    prestamo = db.query(Prestamo).filter_by(id=id).first()
    if not prestamo or prestamo.usuario_id != usuario.id:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    libro = db.query(Libro).get(prestamo.libro_id)
    libro.disponible = True
    db.commit()
    db.refresh(libro)
    return {"msg": "Libro devuelto"}
