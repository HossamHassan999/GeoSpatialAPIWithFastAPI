from fastapi import FastAPI , Depends
from fastapi.responses import JSONResponse
from typing import Optional , Annotated
from enum import Enum
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db import SessionLocal, engine
from models import Item
from services import get_roads_as_geojson , get_roads_as_geojson_ById,get_roads_near_point
from db import get_db    
from schemas.item import FeatureCollection ,Coords
from fastapi import HTTPException





app = FastAPI()


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
    
    
@app.post("/GetDataByCoord", response_model=FeatureCollection)
async def getbycoord(coords: Coords, db: Session = Depends(get_db)):
    item = get_roads_near_point(coords.lon, coords.lat, coords.distance, db)
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="No roads found in this range")