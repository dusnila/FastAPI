from email.message import EmailMessage
from app.config import setting
from pydantic import EmailStr

def create_send_verification_email(
        email_to: EmailStr,
        token: str,
):
    email = EmailMessage()

    email["Subject"] = "Потвердение регистрации"
    email["From"] = setting.SMTP_USER
    email["To"] = email_to

    link = f"http://localhost:8000/auth/verify?token={token}"
    
    email.set_content(f"Нажмите на ссылку для активации: {link}", subtype="html")
    return email