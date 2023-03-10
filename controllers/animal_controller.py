from sqlalchemy.orm import Session
from fastapi import HTTPException

from sql.crud import get_animal, get_type, anim_search


def get_anim_info(animal_id: int, db: Session):
    if not animal_id:
        raise HTTPException(status_code=400)
    if animal_id <= 0:
        raise HTTPException(status_code=400)
    try:
        return get_animal(animal_id, db)
    except:
        raise HTTPException(status_code=404)


def get_info_type(type_id: int, db: Session):
    if not type_id:
        raise HTTPException(status_code=400)
    if type_id <= 0:
        raise HTTPException(status_code=400)
    try:
        return get_type(type_id, db)
    except:
        raise HTTPException(status_code=404)


def search_anim(startDateTime, endDateTime, chipperId, chippingLocationId, lifeStatus, gender, froom, size, db: Session):
    if froom < 0:
        raise HTTPException(status_code=400)
    if size <= 0:
        raise HTTPException(status_code=400)
    if chipperId:
        if chipperId <= 0:
            raise HTTPException(status_code=400)
    if chippingLocationId:
        if chippingLocationId <= 0:
            raise HTTPException(status_code=400)
    if lifeStatus:
        if lifeStatus != 'ALIVE':
            if lifeStatus != 'DEAD':
                raise HTTPException(status_code=400)
    if gender:
        if gender != 'MALE':
            if gender != 'FEMALE':
                if gender != 'OTHER':
                    raise HTTPException(status_code=400)
    return anim_search(startDateTime, endDateTime, chipperId, chippingLocationId, lifeStatus, gender, froom, size, db)
