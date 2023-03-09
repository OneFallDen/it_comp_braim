from fastapi import routing, Depends
from sqlalchemy.orm import Session


from sql.db import get_db
from controllers.location_controller import get_loc_info


router = routing.APIRouter()


@router.get('/locations/{pointId}', tags=['location'])
async def get_location_info(pointId: int, db: Session = Depends(get_db)):
    return get_loc_info(pointId, db)
