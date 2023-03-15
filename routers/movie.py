from fastapi import APIRouter
from fastapi import Body, Path, Query, Depends
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwtbearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

@movie_router.get('/movies',tags=['Movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db=db)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@movie_router.get('/movies/{id}',tags=['Movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1,le=2000)) -> Movie:
    db = Session()
    result = MovieService(db=db).get_movie(id=id)
    if not result:
        return JSONResponse(status_code=404, content={'message':'No encontrado'})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@movie_router.get('/movies/',tags=['Movies'],response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movie_by_category(category=category)
    if not result:
        return JSONResponse(content={'message':'No encontrado'},status_code=404)
    return JSONResponse(content=jsonable_encoder(result),status_code=200)

@movie_router.post('/movies', tags=['Movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie=movie)
    return JSONResponse(content={'message':'Se ha registrado la pelicula'},status_code=201)

@movie_router.put('/movies/{id}',tags=['Movies'], response_model=dict, status_code=200)
def update_movie(id:int = Path(ge=1,le=2000),movie:Movie = Body()) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id=id)
    if not result:
        return JSONResponse(content={'message':'No encontrado'},status_code=404)
    MovieService(db=db).update_movie(id=id,data=movie)
    return JSONResponse(content={'message':'Se ha modificado la pelicula'},status_code=200)

@movie_router.delete('/movies/{id}',tags=['Movies'], response_model=dict,status_code=200)
def delete_movie(id:int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(content={'message':'No encontrado'},status_code=404)
    db.delete(result)
    db.commit()
    return JSONResponse(content={'message':'Se ha eliminado la pelicula'},status_code=200)
