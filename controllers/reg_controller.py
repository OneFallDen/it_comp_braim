from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
import re
from typing import Union

pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
from sql.crud import check_email, signup_user, get_user
from auth.auth import encode_password, verify_password
from sql.db import get_db
from auth.auth import security


def reg_user(firstname: str, lastname: str, email: str, password: str, db: Session):
    if not firstname:
        raise HTTPException(status_code=400)
    if firstname.replace(' ', '') == '':
        raise HTTPException(status_code=400)
    if not lastname:
        raise HTTPException(status_code=400)
    if lastname.replace(' ', '') == '':
        raise HTTPException(status_code=400)
    if not email:
        raise HTTPException(status_code=400)
    if email.replace(' ', '') == '':
        raise HTTPException(status_code=400)
    if re.match(pattern, email) is None:
        raise HTTPException(status_code=400)
    if not password:
        raise HTTPException(status_code=400)
    if password.replace(' ', '') == '':
        raise HTTPException(status_code=400)
    s = 0
    try:
        s = check_email(email, db)
    except:
        d = 1
    if s > 0:
        raise HTTPException(status_code=409)
    hashed_password = encode_password(password)
    user_id = signup_user(firstname, lastname, email, hashed_password, db)
    return {
        'id': user_id,
        'firstname': firstname,
        'lastname': lastname,
        'email': email
    }


async def get_current_account(db: Session = Depends(get_db),
                              credentials: Union[HTTPBasicCredentials, None] = Depends(security),
                              ):
    if not credentials:
        return None
    try:
        user = get_user(credentials.username, db)
    except:
        raise HTTPException(status_code=401)
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401)
    return user
