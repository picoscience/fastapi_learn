from pydantic import BaseModel, Field
from typing import Optional

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