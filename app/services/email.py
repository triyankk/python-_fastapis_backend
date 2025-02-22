from typing import Any, Dict
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from ..core.config import settings
from pathlib import Path

conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.EMAILS_FROM_EMAIL,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_TLS=settings.SMTP_TLS,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / "email-templates"
)

async def send_email(
    email_to: str,
    subject: str,
    template_name: str,
    environment: Dict[str, Any]
) -> None:
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=environment,
        subtype="html"
    )
    
    fm = FastMail(conf)
    await fm.send_message(message, template_name=template_name)

async def send_verification_email(email_to: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Email Verification"
    
    await send_email(
        email_to=email_to,
        subject=subject,
        template_name="verification.html",
        environment={
            "project_name": project_name,
            "verification_url": f"{settings.SERVER_HOST}/verify-email/{token}"
        }
    )

async def send_password_reset_email(email_to: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password Reset"
    
    await send_email(
        email_to=email_to,
        subject=subject,
        template_name="reset_password.html",
        environment={
            "project_name": project_name,
            "reset_url": f"{settings.SERVER_HOST}/reset-password/{token}"
        }
    )
