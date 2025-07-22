from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class Prestamo(Base):
    __tablename__ = "prestamos"

    id = Column(Integer, primary_key=True, index=True)
    libro_id = Column(Integer, ForeignKey("libros.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha_prestamo = Column(String)
    fecha_devolucion = Column(String)