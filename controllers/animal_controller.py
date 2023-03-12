from sqlalchemy.orm import Session
from fastapi import HTTPException

from sql.crud import get_animal, get_type, anim_search, check_type, add_type, type_update, delete_type, \
    check_animal_type, get_account, get_location, add_anim, get_animal_status, update_anim
from sql import models


def check_gender(gender: str):
    if gender != 'MALE':
        if gender != 'FEMALE':
            if gender != 'OTHER':
                raise HTTPException(status_code=400)


def valid_float(a: float):
    if not a:
        raise HTTPException(status_code=400)
    if a <= 0:
        raise HTTPException(status_code=400)


def valid_integers(a: int):
    if not a:
        raise HTTPException(status_code=400)
    if a <= 0:
        raise HTTPException(status_code=400)


def check_lifestatus(a: str):
    if a != 'ALIVE':
        if a != 'DEAD':
            raise HTTPException(status_code=400)


def check_user(a: int, db: Session):
    try:
        get_account(a, db)
    except:
        raise HTTPException(status_code=404)


def valid_animal(a: int, db: Session):
    try:
        get_animal(a, db)
    except:
        raise HTTPException(status_code=404)


def valid_location(a: int, db):
    try:
        get_location(a, db)
    except:
        raise HTTPException(status_code=404)


def animal_update(animalId: int, weight: float, length: float, height: float, gender: str, lifeStatus: str, chipperId: int,
               chippingLocationId: int, user: models.Account, db: Session):
    valid_integers(animalId)
    valid_float(weight)
    valid_float(length)
    valid_float(height)
    check_gender(gender)
    check_lifestatus(lifeStatus)
    check_gender(gender)
    valid_integers(chipperId)
    valid_integers(chippingLocationId)
    check_user(chipperId, db)
    valid_animal(animalId, db)
    valid_location(chippingLocationId, db)
    if lifeStatus == 'ALIVE':
        status = get_animal_status(animalId, db)
        if status == 'DEAD':
            raise HTTPException(status_code=400)
    return update_anim(animalId, weight, length, height, gender, lifeStatus, chipperId, chippingLocationId, db)


def animal_add(animalTypes: [], weight: float, length: float, height: float, gender: str, chipperId: int,
               chippingLocationId: int, user: models.Account, db: Session):
    if not animalTypes:
        raise HTTPException(status_code=400)
    if len(animalTypes) <= 0:
        raise HTTPException(status_code=400)
    for at in animalTypes:
        if not at:
            raise HTTPException(status_code=400)
        if at <= 0:
            raise HTTPException(status_code=400)
        try:
            get_type(at, db)
        except:
            raise HTTPException(status_code=400)
    valid_float(weight)
    valid_float(length)
    valid_float(height)
    check_gender(gender)
    valid_integers(chipperId)
    valid_integers(chippingLocationId)
    try:
        get_account(chipperId, db)
    except:
        raise HTTPException(status_code=404)
    try:
        get_location(chippingLocationId, db)
    except:
        raise HTTPException(status_code=404)
    setarr = set(animalTypes)
    if not len(animalTypes) == len(setarr):
        raise HTTPException(status_code=409)
    return add_anim(animalTypes, weight, length, height, gender, chipperId, chippingLocationId, db)


def animal_type_delete(typeId: int, user: models.Account, db: Session):
    if not typeId:
        raise HTTPException(status_code=400)
    if typeId <= 0:
        raise HTTPException(status_code=400)
    s = 0
    try:
        res = check_animal_type(typeId, db)
        if res:
            s = 1
    except:
        pass
    if s > 0:
        raise HTTPException(status_code=400)
    try:
        get_type(typeId, db)
    except:
        raise HTTPException(status_code=404)
    delete_type(typeId, db)


def animal_type_update(typeId: int, type: str, user: models.Account, db: Session):
    if not type:
        raise HTTPException(status_code=400)
    if type.replace(' ', '') == '':
        raise HTTPException(status_code=400)
    if not typeId:
        raise HTTPException(status_code=400)
    if typeId <= 0:
        raise HTTPException(status_code=400)
    try:
        get_type(typeId, db)
    except:
        raise HTTPException(status_code=404)
    return type_update(typeId, type, db)


def animal_type_add(type: str, user: models.Account, db: Session):
    if not type:
        raise HTTPException(status_code=400)
    if type.replace(' ', '') == '':
        raise HTTPException(status_code=400)
    s = 0
    try:
        res = check_type(type, db)
        if res:
            s = 1
    except:
        pass
    if s > 0:
        raise HTTPException(status_code=409)
    return add_type(type, db)


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
