from fastapi import FastAPI
from fastapi.responses import HTMLResponse 
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

"""
uvicorn main:app --reload --port 5000 --host 0.0.0.0
VALIDACION: Parametros Query, Path y Field(clases, esquemas)

-----CRUD-----
CREATE: post
READ:   get
UPDATE: put
DELETE: delete
--------------

-------HTTP Response codes-------
Informational responses (100-199)
Successful responses    (200-299)
Redirection message     (300-399)
Client error responses  (400-499)
Server error responses  (500-599)
---------------------------------

PyJWT (Python JSON Web Token) es una biblioteca de Python que se utiliza para codificar y decodificar tokens JWT (JSON Web Token). Un token JWT es un objeto de seguridad que se utiliza para autenticar a los usuarios en aplicaciones web y móviles. Los tokens JWT se emiten por un servidor de autenticación y luego se envían al cliente, que los utiliza para demostrar su identidad al acceder a recursos protegidos en el servidor

SQLModel (facilidad creacion esquemas y modelos)
https://sqlmodel.tiangolo.com/

"""

app = FastAPI()
app.title = 'Documentación con FastAPI'
app.version = '0.0.1'

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)


@app.get('/',tags=['Home'])
def message():
    return HTMLResponse('<h1 style=color:black>Hellow World!</h1>')

