from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from routers import Libro, Prestamo,auth, Dev
from models.usuario import Usuario
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind = engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(Libro.router)
app.include_router(Prestamo.router)
app.include_router(Dev.router)

@app.get("/", response_class = HTMLResponse)
async def home ():
    return HTMLResponse (content="<h1>Bienvenida a la Biblioteca</h1>", status_code=200)


origins = [
    "*",  # Permite todos los orígenes, para desarrollo
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
