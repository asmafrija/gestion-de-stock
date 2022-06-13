from optparse import Option
from typing import Optional
import uuid
from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session

from app import oauth2
from app.models import user
from ..routers.confirmation_code import add_confirmation_code
from ..routers.mailSender import send_email
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

async def sendConfirmationMail(email: str, db: any):
    confirmation_code_to_add = schemas.ConfirmationCodeCreate(email = email, confirmation_code = str(uuid.uuid1()), status = '1')
    await add_confirmation_code(confirmation_code_to_add, db)

    subject = "Account Confirmation"
    recipients = [email]
    message = utils.confirm_mail_template.format(confirmation_code_to_add.confirmation_code)

    await send_email(subject,recipients,message)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        return {"message": f"email already used", "status": status.HTTP_400_BAD_REQUEST}

    if user.password != user.confirm_password:
        return {"message": f"Passwords must match !", "status": status.HTTP_400_BAD_REQUEST}

    hashed_password = utils.hash(user.password)

    new_user = models.User(name=user.name, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    user_result = schemas.UserOut(**new_user.__dict__)
    user_result.status = status.HTTP_201_CREATED
    await sendConfirmationMail(user.email, db)
    user_result.message = "Confirmation email sent"
    return user_result


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        return {"message": f"User with id: {id} does not exist", "status": status.HTTP_404_NOT_FOUND}

    return user

@router.get('/', response_model=schemas.UsersOut)
def get_users(db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user), nameSubstring: Optional[str] = ""):
    users = db.query(models.User).filter(models.User.name.contains(nameSubstring)).all()
    
    return schemas.UsersOut(list=[schemas.UserOut(**user.__dict__) for user in users],
                        status=status.HTTP_200_OK)
