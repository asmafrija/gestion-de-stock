from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class UserOut(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    creation_date: Optional[datetime] = None
    is_active: Optional[bool] = None
    is_confirmed: Optional[bool] = None
    message: Optional[str] = None
    status: Optional[int] = None

    class Config:
        orm_mode = True

class UsersOut(BaseModel):
    list: Optional[List[UserOut]] = []
    message: Optional[str] = None
    status: Optional[int] = None

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    confirm_password: str

class UserConfirm(BaseModel):
    is_confirmed: bool

class UserResetPassword(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    message: Optional[str] = None
    status: Optional[int] = None
    user_id: Optional[int] = None
    user_name: Optional[str] = None

class TokenData(BaseModel):
    id: Optional[str] = None

class ForgotPassword(BaseModel):
    email: EmailStr

class ForgotPasswordOut(BaseModel):
    message: Optional[str] = None
    status: Optional[int] = None

class EmailSchema(BaseModel):
    email: List[EmailStr]

class ResetCodeCreate(BaseModel):
    email: EmailStr
    reset_code: str
    status: str

class ConfirmationCodeCreate(BaseModel):
    email: EmailStr
    confirmation_code: str
    status: str

class ResetPassword(BaseModel):
    reset_password_code: str
    new_password: str
    confirm_new_password: str

class ResetPasswordOut(BaseModel):
    message: str
    status: int

class SendConfirmationMail(BaseModel):
    email: EmailStr

class ConfirmAccount(BaseModel):
    confirmation_code: str

class ConfirmAccountOut(BaseModel):
    message: str
    status: int

class PhotoCreate(BaseModel):
    photo_url: str
    dog_id: int

class PhotoOut(BaseModel):
    id: Optional[int] = None
    photo_url: Optional[str] = None
    dog_id : Optional[int] = None
    creation_date: Optional[datetime] = None
    message: Optional[str] = None
    status: Optional[int] = None

class PhotosOut(BaseModel):
    list: List[PhotoOut]=[]
    message: Optional[str] = None
    status: Optional[int] = None

class ProductCreate(BaseModel):
    name : str
    lot_number : str
    quantity : int
    temperature : float

class ProductOut(BaseModel):
    id : Optional[int] = None
    name : Optional[str] = None
    lot_number : Optional[str] = None
    quantity : Optional[int] = None
    temperature : Optional[float] = None
    message: Optional[str] = None
    status: Optional[int] = None

class ProductsOut(BaseModel):
    list: Optional[List[ProductOut]] = []
    message: Optional[str] = None
    status: Optional[int] = None


