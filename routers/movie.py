from fastapi import APIRouter
from fastapi import Body, Path, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwtbearer import JWTBearer
from services.movie import MovieService

movie_router = APIRouter()

class Movie(BaseModel):
#   id: int | None = None
    id: Optional[int]
    title: str = Field(min_length=5, max_length=25)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2025)#less or equal than 2022
    rating: float = Field(ge=1,le=10)
    category: str = Field(min_length=2, max_length=20)

    class Config:
        schema_extra = {
            'example':{
                'id':1,
                'title':'Texto',
                'overview':'Descripcion de la pelicula',
                'year':2023,
                'rating':10,
                'category':'Acción'
            }
        }

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
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
        return JSONResponse(content={'message':'No encontrado'},status_code=404)
    return JSONResponse(content=jsonable_encoder(result),status_code=200)

@movie_router.post('/movies', tags=['Movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(content={'message':'Se ha registrado la pelicula'},status_code=201)

@movie_router.put('/movies/{id}',tags=['Movies'], response_model=dict, status_code=200)
def update_movie(id:int = Path(ge=1,le=2000),movie:Movie = Body()) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(content={'message':'No encontrado'},status_code=404)
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
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
