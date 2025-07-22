from pydantic import BaseModel

class PrestamoCreate(BaseModel):
    id: int
    libro_id: int
    usuario_id: int
    fecha_prestamo: str
    fecha_devolucion: str

class PrestamoOut(BaseModel):
    id: int
    libro_id: int
    usuario_id: int
    fecha_prestamo: str
    fecha_devolucion: str

    class Config:
        orm_mode = True
