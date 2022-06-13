from datetime import timedelta, datetime
from sqlalchemy import and_
from .. import schemas, models
from fastapi import status, HTTPException

async def add_reset_code(reset_code: schemas.ResetCodeCreate, db: any):

    new_reset_code = models.ResetCode(**reset_code.dict())
    db.add(new_reset_code)
    db.commit()
    db.refresh(new_reset_code)

    return new_reset_code

async def check_reset_password_code(reset_code: str, db: any):
    date = datetime.utcnow() + timedelta(minutes=-120)
    return db.query(models.ResetCode).filter(
        and_(and_(models.ResetCode.expired_in >= date, models.ResetCode.status == '1'),
            models.ResetCode.reset_code == reset_code)).first()

async def reset_password(email: str, new_hashed_password: str, db: any):
    user_query = db.query(models.User).filter(models.User.email == email)
    user = user_query.first()
    if not user:
        schemas.ResetPasswordOut(message="No user with this email",
                                status=status.HTTP_404_NOT_FOUND)
    user_to_update = schemas.UserResetPassword(email=user.email, password=new_hashed_password)
    user_query.update(user_to_update.dict(), synchronize_session=False)
    db.commit()

    return user_query.first()

async def disable_reset_code(reset_code: str, db: any):
    reset_code_query = db.query(models.ResetCode).filter(models.ResetCode.reset_code == reset_code)
    code = reset_code_query.first()
    if not code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"This reset code doesn't exist")
    reset_code_query_to_update = schemas.ResetCodeCreate(email=code.email, reset_code=code.reset_code, status='0')
    reset_code_query.update(reset_code_query_to_update.dict(), synchronize_session=False)
    db.commit()

    return reset_code_query.first()