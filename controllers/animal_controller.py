from sqlalchemy.orm import Session
from fastapi import HTTPException

from sql.crud import get_animal, get_type


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
