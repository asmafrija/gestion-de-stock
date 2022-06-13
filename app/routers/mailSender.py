from typing import List
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from ..config import settings


conf = ConnectionConfig(
    MAIL_USERNAME = settings.mail_username,
    MAIL_PASSWORD = settings.mail_password,
    MAIL_FROM = settings.mail_from,
    MAIL_PORT = 587,
    MAIL_SERVER = settings.mail_server,
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_email(subject: str, recipients: List, message: str):

    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=message,
        subtype="html"
        )

    fm = FastMail(conf)
    await fm.send_message(message)

