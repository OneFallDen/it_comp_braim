from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from sql.crud import get_location, get_animal, loc_search, get_animal_status, last_visit_point, add_visit_point


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
