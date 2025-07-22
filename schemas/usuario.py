from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    email: str
    password: str

class UsuarioOut(BaseModel):
    id: int
    email: str
    class Config:
        orm_mode = True
