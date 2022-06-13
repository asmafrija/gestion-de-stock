import uuid
from fastapi import APIRouter, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..routers.confirmation_code import check_confirmation_code, confirm_account, disable_confirmation_code
from ..routers.mailSender import send_email
from ..routers.reset_code import add_reset_code, check_reset_password_code, disable_reset_code, reset_password
from app.utils import reset_password_mail_template

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    unauthorized_return = schemas.Token(message="Invalid Credentials",
                            status=status.HTTP_401_UNAUTHORIZED)

    if not user:
        return unauthorized_return

    if not user.is_confirmed:
        return schemas.Token(message="Email hasn't been verified yet",
                            status=status.HTTP_403_FORBIDDEN)

    if not utils.verify(user_credentials.password, user.password):
        return unauthorized_return

    return schemas.Token(access_token=oauth2.create_access_token(data={"user_id": user.id}), 
                token_type="bearer", 
                status=status.HTTP_200_OK,
                user_id=user.id,
                user_name=user.name)


@router.post('/forgotPassword', response_model=schemas.ForgotPasswordOut)
async def forgotPassword(user: schemas.ForgotPassword, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user.email).first()

    if not user:
        return schemas.ForgotPasswordOut(message="No account with this email",
                        status=status.HTTP_404_NOT_FOUND)

    reset_code_to_add = schemas.ResetCodeCreate(email = user.email, reset_code = str(uuid.uuid1()), status = '1')
    await add_reset_code(reset_code_to_add, db)

    subject = "Reset Password"
    recipients = [user.email]
    message = reset_password_mail_template.format(reset_code_to_add.reset_code)

    await send_email(subject,recipients,message)

    return schemas.ForgotPasswordOut(message="email sent!",
                        status=status.HTTP_200_OK)

@router.patch('/resetPassword', response_model=schemas.ResetPasswordOut)
async def resetPassword(request: schemas.ResetPassword, db: Session = Depends(database.get_db)):
    reset_code = await check_reset_password_code(request.reset_password_code, db)
    if not reset_code:
        return schemas.ResetPasswordOut(message="Reset Link Expired",
                                status=status.HTTP_400_BAD_REQUEST)

    if request.new_password != request.confirm_new_password:
        return schemas.ResetPasswordOut(message="New password is not match !",
                                status=status.HTTP_400_BAD_REQUEST)

    new_hashed_password = utils.hash(request.new_password)
    await reset_password(reset_code.email, new_hashed_password, db)
    await disable_reset_code(reset_code.reset_code, db)

    return schemas.ResetPasswordOut(message="password reset succefully !",
                                status=status.HTTP_200_OK)

@router.patch('/confirmAccount', response_model=schemas.ConfirmAccountOut)
async def confirmAccount(request: schemas.ConfirmAccount, db: Session = Depends(database.get_db)):
    confirmation_code = await check_confirmation_code(request.confirmation_code, db)
    if not confirmation_code:
        return schemas.ConfirmAccountOut(message="Reset Link doesn't exist",
                                status=status.HTTP_400_BAD_REQUEST)

    await confirm_account(confirmation_code.email, db)
    await disable_confirmation_code(confirmation_code.confirmation_code, db)

    return schemas.ConfirmAccountOut(message="Account confirmed !",
                                status=status.HTTP_200_OK)
