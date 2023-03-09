from fastapi import routing, Depends
from sqlalchemy.orm import Session


from sql.db import get_db
from controllers.account_controller import get_acc_info


router = routing.APIRouter()


@router.get('/accounts/{accountId}', tags=['account'])
async def get_account_info(accountId: int, db: Session = Depends(get_db)):
    return get_acc_info(accountId, db)
