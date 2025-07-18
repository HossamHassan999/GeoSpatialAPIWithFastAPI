from fastapi import FastAPI , Depends
from fastapi.responses import JSONResponse
from typing import Optional , Annotated
from enum import Enum
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer


app = FastAPI()

# @app.get("/")
# async def root():
#     return {"message":"welcom evry body"}


# @app.post("/")
# async def root():
#     return {"message":"Done post !"}


# @app.get("/users")
# async def usera_liat():
#     return ["ahmed", "mohamed", "nada"]

# @app.get("/users/{userid}")
# async def GetUsersById(userid: int):
#     if userid == 1 :
        
#         return JSONResponse(status_code=200 ,content= {"name ":"Ahmed"})
    
#     else: 
#         return JSONResponse(status_code=404 ,content= {"error ":"not found"})
        
        


# items = [
#     {"id":1 , "name":"book" , "price":"15" , "stock": True},
#     {"id":2 , "name":"game" , "price":"50" , "stock": True},
#     {"id":3 , "name":"cd" , "price":"30" , "stock": True},
#     {"id":4 , "name":"magazine" , "price":"10" , "stock": False},
#     {"id":5 , "name":"book" , "price":"10" , "stock": True},
#     {"id":6 , "name":"game" , "price":"10" , "stock": True}
# ]


# @app.get("/filter")
# async def filterbyvalue(name: Optional[str]=None):
#     for i in items :
#         if i['name'] == name:
#             return i
        
#     return {"message": "Item not found"}
        


# class Days(Enum):
#     sunday = 1
#     monday = 2
#     tuesday = 3
    
# @app.get("/Days")
# async def getdaybunum(id : Optional[int]=None):
#     for i in Days :
#         if i.value == id :
#             return i.name



# class Person(BaseModel):
#     name : str
#     age : int 
#     salary : float | None = None
#     is_marid : bool

# @app.post("/person")
# async def create_person(person : Person):
#     return person
    
    
    
    
from sqlalchemy.orm import Session
from db import SessionLocal, engine
from models import Item
from services import get_roads_as_geojson , get_roads_as_geojson_ById,get_roads_near_point
from db import get_db    
from schemas.item import FeatureCollection ,Coords
from fastapi import HTTPException

        
        

@app.get("/items")
async def read_items(db: Session = Depends(get_db)):
    items =  get_roads_as_geojson(db)
    return items


@app.get("/items/{id}",response_model=FeatureCollection)
async def getbyid(id:int ,db : Session = Depends(get_db) ):
    item = get_roads_as_geojson_ById(id,db)
    if item :
        return item
    else:
        return {"message":"Not Found !"}
    
    
@app.post("/GetDataByCoor", response_model=FeatureCollection)
async def getbycoord(coords: Coords, db: Session = Depends(get_db)):
    item = get_roads_near_point(coords.lon, coords.lat, coords.distance, db)
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="No roads found in this range")