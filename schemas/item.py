from pydantic import BaseModel
from typing import Optional, List

class Geometry(BaseModel):
    type: str
    coordinates: List

class RoadProperties(BaseModel):
    id: int
    name: Optional[str] = None

class Feature(BaseModel):
    type: str = "Feature"
    geometry: Geometry
    properties: RoadProperties

class FeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List[Feature]
    
    
class Coords(BaseModel):
    lon: float= 31.34634
    lat: float = 30.053531
    distance: float = 10



