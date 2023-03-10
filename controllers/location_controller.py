from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from sql.crud import get_location, get_animal, loc_search


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
