# from pathlib import Path
from app.config import setting
from pydantic import EmailStr
from app.tasks.celery import celery
import smtplib

from app.tasks.email_templates import create_send_verification_email


@celery.task
def send_verification_email(
    email_to: EmailStr,
    veryfication_token: str
):
    
    msg_content = create_send_verification_email(email_to, veryfication_token)

    with smtplib.SMTP_SSL(setting.SMTP_HOST, setting.SMTP_PORT) as server:
        server.login(setting.SMTP_USER, setting.SMTP_PASS)
        server.send_message(msg_content)