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
from models import User
from schemas.user import UserCreate
from auth import get_password_hash
from fastapi.security import OAuth2PasswordRequestForm
from auth import authenticate_user, create_access_token
from auth import get_current_user





app = FastAPI()
road_util = RoadUtility()



@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")

    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}




@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }




@app.get("/items")
async def read_items(db: Session = Depends(get_db) , current_user: User = Depends(get_current_user)):
    items =  road_util.get_roads_as_geojson(db)
    return items


@app.get("/items/{id}",response_model=FeatureCollection)
async def getbyid(id:int ,db : Session = Depends(get_db) ,current_user: User = Depends(get_current_user)):
    item = road_util.get_roads_as_geojson_ById(id,db)
    if item :
        return item
    else:
        return {"message":"Not Found !"}
    
    
@app.post("/GetDataByCoord", response_model=FeatureCollection)
async def getbycoord(coords: Coords, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    item = road_util.get_roads_near_point(coords.lon, coords.lat, coords.distance, db)
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="No roads found in this range")