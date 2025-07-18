from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Item
import json
from geoalchemy2.elements import WKTElement




def MakeGeoJson(result):
    
    features = []
    for row in result:
        feature = {
            "type": "Feature",
            "geometry": json.loads(row.geometry),
            "properties": {
                "id": row.id,
                "name": row.name
            }
        }
        features.append(feature)
        
    return {
        "type": "FeatureCollection",
        "features": features
    }
    
   
    
class RoadUtility:
            
    def get_roads_as_geojson(self,db: Session):
        result = db.query(
            Item.id,
            Item.name,
            func.ST_AsGeoJSON(Item.geom).label("geometry")
        ).limit(50).all()
        
        return  MakeGeoJson(result)



    def get_roads_as_geojson_ById(self,id:int, db: Session):
        result = db.query(
            Item.id,
            Item.name,
            func.ST_AsGeoJSON(Item.geom).label("geometry")
        ).filter(Item.id==id).first()
        
        return  MakeGeoJson([result])




    def get_roads_near_point(self,lon: float, lat: float, distance: float, db: Session):
        
        point_wkt = func.ST_GeomFromText(f'POINT({lon} {lat})', srid=4326)

        result = db.query(
            Item.id,
            Item.name,
            func.ST_AsGeoJSON(Item.geom).label("geometry")
        ).filter(
            func.ST_DWithin(
                func.Geography(Item.geom), 
                func.Geography(point_wkt), 
                distance    
            )
            
        ).all()

        return MakeGeoJson(result)

