from pydantic import BaseModel


class LibroCreate(BaseModel):
    titulo: str
    autor: str

class LibroOut(BaseModel):
    id: int
    autor: str
    disponible: bool
    class Config:
        orm_mode = True
