from fastapi import FastAPI , Depends
from fastapi.responses import JSONResponse
from typing import Optional , Annotated
from enum import Enum
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db import SessionLocal, engine
from models import Item
from services import RoadUtility 
from db import get_db    
from schemas.item import FeatureCollection ,Coords
from fastapi import HTTPException





app = FastAPI()
road_util = RoadUtility()


@app.get("/items")
async def read_items(db: Session = Depends(get_db)):
    items =  road_util.get_roads_as_geojson(db)
    return items


@app.get("/items/{id}",response_model=FeatureCollection)
async def getbyid(id:int ,db : Session = Depends(get_db) ):
    item = road_util.get_roads_as_geojson_ById(id,db)
    if item :
        return item
    else:
        return {"message":"Not Found !"}
    
    
@app.post("/GetDataByCoord", response_model=FeatureCollection)
async def getbycoord(coords: Coords, db: Session = Depends(get_db)):
    item = road_util.get_roads_near_point(coords.lon, coords.lat, coords.distance, db)
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="No roads found in this range")