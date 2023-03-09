from sqlalchemy.orm import Session
from fastapi import HTTPException

from sql.crud import get_location


def get_loc_info(point_id: int, db: Session):
    if not point_id:
        raise HTTPException(status_code=400)
    if point_id <= 0:
        raise HTTPException(status_code=400)
    try:
        return get_location(point_id, db)
    except:
        raise HTTPException(status_code=404)

