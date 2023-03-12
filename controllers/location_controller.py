from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from sql.crud import get_location, get_animal, loc_search, get_animal_status, last_visit_point, add_visit_point,\
    get_visited_location, check_visited_point, update_point_visit, delete_visited_point, check_location, add_loc
from sql import models


def location_add(latitude: float, longitude: float, user: models.Account, db: Session):
    if not latitude:
        raise HTTPException(status_code=400)
    if latitude < -90:
        raise HTTPException(status_code=400)
    if latitude > 90:
        raise HTTPException(status_code=400)
    if not longitude:
        raise HTTPException(status_code=400)
    if longitude < -180:
        raise HTTPException(status_code=400)
    if longitude > 180:
        raise HTTPException(status_code=400)
    s = 0
    try:
        res = check_location(latitude, longitude, db)
        if res:
            s = 1
    except:
        pass
    if s > 0:
        raise HTTPException(status_code=409)
    return add_loc(latitude, longitude, db)


def point_visit_add(animalId: int, pointId: int, db: Session):
    if not pointId:
        raise HTTPException(status_code=400)
    if pointId <= 0:
        raise HTTPException(status_code=400)
    if not animalId:
        raise HTTPException(status_code=400)
    if animalId <= 0:
        raise HTTPException(status_code=400)
    try:
        animal = get_animal(animalId, db)
    except:
        raise HTTPException(status_code=404)
    try:
        get_location(pointId, db)
    except:
        raise HTTPException(status_code=404)
    status = get_animal_status(animalId, db)
    if status == 'DEAD':
        raise HTTPException(status_code=400)
    if animal['chippingLocationId'] == pointId:
        raise HTTPException(status_code=400)
    s = last_visit_point(animalId, db)
    if s.loc_id == pointId:
        raise HTTPException(status_code=400)
    return add_visit_point(animalId, pointId, db)


def visited_point_delete(animalId: int, visitedPointId: int, db: Session):
    if not animalId:
        raise HTTPException(status_code=400)
    if animalId <= 0:
        raise HTTPException(status_code=400)
    if not visitedPointId:
        raise HTTPException(status_code=400)
    if visitedPointId <= 0:
        raise HTTPException(status_code=400)
    try:
        animal = get_animal(animalId, db)
    except:
        raise HTTPException(status_code=404)
    try:
        get_visited_location(visitedPointId, db)
    except:
        raise HTTPException(status_code=404)
    try:
        s = check_visited_point(animalId, visitedPointId, db)
        if not s:
            raise HTTPException(status_code=404)
    except:
        raise HTTPException(status_code=404)
    return delete_visited_point(animalId, visitedPointId, db)


def point_visit_update(animalId: int, visitedLocationPointId: int, locationPointId: int, db: Session):
    if not animalId:
        raise HTTPException(status_code=400)
    if animalId <= 0:
        raise HTTPException(status_code=400)
    if not visitedLocationPointId:
        raise HTTPException(status_code=400)
    if visitedLocationPointId <= 0:
        raise HTTPException(status_code=400)
    if not locationPointId:
        raise HTTPException(status_code=400)
    if locationPointId <= 0:
        raise HTTPException(status_code=400)
    try:
        animal = get_animal(animalId, db)
    except:
        raise HTTPException(status_code=404)
    try:
        get_visited_location(visitedLocationPointId, db)
    except:
        raise HTTPException(status_code=404)
    try:
        check_visited_point(animalId, visitedLocationPointId, db)
    except:
        raise HTTPException(status_code=404)
    try:
        get_location(locationPointId, db)
    except:
        raise HTTPException(status_code=404)
    if visitedLocationPointId == 1:
        if animal['chippingLocationId'] == locationPointId:
            raise HTTPException(status_code=400)
    res = get_visited_location(visitedLocationPointId, db)
    if res.loc_id == locationPointId:
        raise HTTPException(status_code=400)
    if locationPointId in animal['visitedLocations']:
        raise HTTPException(status_code=400)
    return update_point_visit(animalId, visitedLocationPointId, locationPointId, db)


def get_loc_info(point_id: int, db: Session):
    if not point_id:
        raise HTTPException(status_code=400)
    if point_id <= 0:
        raise HTTPException(status_code=400)
    try:
        return get_location(point_id, db)
    except:
        raise HTTPException(status_code=404)


def search_loc(animalId: int, startDateTime, endDateTime, froom, size, db: Session):
    if froom < 0:
        raise HTTPException(status_code=400)
    if size <= 0:
        raise HTTPException(status_code=400)
    if not animalId:
        raise HTTPException(status_code=400)
    if animalId <= 0:
        raise HTTPException(status_code=400)
    try:
        get_animal(animalId, db)
    except:
        raise HTTPException(status_code=404)
    return loc_search(animalId, startDateTime, endDateTime, froom, size, db)
