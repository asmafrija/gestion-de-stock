from datetime import timedelta, datetime
from sqlalchemy import and_
from .. import schemas, models
from fastapi import status, HTTPException

async def add_confirmation_code(confirmation_code: schemas.ConfirmationCodeCreate, db: any):

    new_confirmation_code = models.ConfirmationCode(**confirmation_code.dict())
    db.add(new_confirmation_code)
    db.commit()
    db.refresh(new_confirmation_code)

    return new_confirmation_code

async def check_confirmation_code(confirmation_code: str, db: any):
    return db.query(models.ConfirmationCode).filter(
        and_(models.ConfirmationCode.confirmation_code == confirmation_code, 
        models.ResetCode.status == '1')).first()

async def confirm_account(email: str, db: any):
    user_query = db.query(models.User).filter(models.User.email == email)
    user = user_query.first()
    if not user:
        schemas.ResetPasswordOut(message="No user with this email",
                                status=status.HTTP_404_NOT_FOUND)

    user_to_update = schemas.UserConfirm(is_confirmed=True)
    user_query.update(user_to_update.dict(), synchronize_session=False)
    db.commit()

    return user_query.first()

async def disable_confirmation_code(confirmation_code: str, db: any):
    confirmation_code_query = db.query(models.ConfirmationCode).filter(models.ConfirmationCode.confirmation_code == confirmation_code)
    code = confirmation_code_query.first()
    if not code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"This confirmation code doesn't exist")
    confirmation_code_query_to_update = schemas.ConfirmationCodeCreate(email=code.email, confirmation_code=code.confirmation_code, status='0')
    confirmation_code_query.update(confirmation_code_query_to_update.dict(), synchronize_session=False)
    db.commit()

    return confirmation_code_query.first()
