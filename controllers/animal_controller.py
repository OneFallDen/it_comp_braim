from sqlalchemy.orm import Session
from fastapi import HTTPException

from sql.crud import get_animal


def get_anim_info(animal_id: int, db: Session):
    if not animal_id:
        raise HTTPException(status_code=400)
    if animal_id <= 0:
        raise HTTPException(status_code=400)
    #try:
    return get_animal(animal_id, db)
    #except:
        #raise HTTPException(status_code=404)
