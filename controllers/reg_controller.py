from sqlalchemy.orm import Session
from fastapi import HTTPException
import re

pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
from sql.crud import check_email, signup_user
from auth.auth import encode_password


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


"""
async def get_current_account(db: Session = Depends(get_db),
    credentials: HTTPBasicCredentials | None = Depends(security),
) -> schemas.Account | None:
    if not credentials:
        return None
    user = get_user(db, credentials.username)
    if not user or not verify_password(credentials.password, user.password):  # type: ignore
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return validate_account(user)
"""
