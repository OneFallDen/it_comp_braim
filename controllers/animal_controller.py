from sqlalchemy.orm import Session
from fastapi import HTTPException

from sql.crud import get_animal, get_type, anim_search, check_type, add_type, type_update, delete_type, \
    check_animal_type, get_account, get_location, add_anim, get_animal_status, update_anim, last_visit_point, \
    delete_anim, check_exsists_type_animal, update_anim_types, type_from_anim_delete, add_anim_type
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


def valid_type(a: int, db: Session):
    try:
        get_type(a, db)
    except:
        raise HTTPException(status_code=404)


def type_from_animal_delete(animalId: int, typeId: int, db: Session):
    valid_integers(animalId)
    valid_integers(typeId)
    valid_animal(animalId, db)
    valid_type(typeId, db)
    try:
        check_exsists_type_animal(animalId, typeId, db)
    except:
        raise HTTPException(status_code=404)
    type_from_anim_delete(animalId, typeId, db)
    return get_animal(animalId, db)


def animal_types_update(animalId: int, oldTypeId: int, newTypeId: int, user: models.Account, db: Session):
    valid_integers(animalId)
    valid_integers(oldTypeId)
    valid_integers(newTypeId)
    valid_type(oldTypeId, db)
    valid_type(newTypeId, db)
    valid_animal(animalId, db)
    s = 0
    try:
        res = check_exsists_type_animal(animalId, newTypeId, db)
        if res:
            s = 1
    except:
        pass
    if s > 0:
        raise HTTPException(status_code=409)
    update_anim_types(animalId, oldTypeId, newTypeId, db)
    return get_animal(animalId, db)


def type_to_animal_add(animalId: int, typeId: int, user: models.Account, db: Session):
    valid_integers(animalId)
    valid_integers(typeId)
    valid_animal(animalId, db)
    valid_type(typeId, db)
    s = 0
    try:
        res = check_exsists_type_animal(animalId, typeId, db)
        if res:
            s = 1
    except:
        pass
    if s > 0:
        raise HTTPException(status_code=409)
    add_anim_type(animalId, typeId, db)
    return get_animal(animalId, db)


def animal_delete(animalId: int, user: models.Account,
                     db: Session):
    valid_integers(animalId)
    valid_animal(animalId, db)
    animal = get_animal(animalId, db)
    last_point = last_visit_point(animalId, db)
    if last_point.loc_id != animal['chippingLocationId']:
        raise HTTPException(status_code=400)
    delete_anim(animalId, db)


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
            raise HTTPException(status_code=404)
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
    valid_integers(typeId)
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
    if type.strip() == '':
        raise HTTPException(status_code=400)
    valid_integers(typeId)
    try:
        get_type(typeId, db)
    except:
        raise HTTPException(status_code=404)
    s = 0
    try:
        res = check_type(type, db)
        if res:
            s = 1
    except:
        pass
    if s > 0:
        raise HTTPException(status_code=409)
    return type_update(typeId, type, db)


def animal_type_add(type: str, db: Session):
    if not type:
        raise HTTPException(status_code=400)
    if type.replace(' ', '') == '':
        raise HTTPException(status_code=400)
    if type.strip() == '':
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
    valid_integers(animal_id)
    try:
        return get_animal(animal_id, db)
    except:
        raise HTTPException(status_code=404)


def get_info_type(type_id: int, db: Session):
    valid_integers(type_id)
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