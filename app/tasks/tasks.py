import smtplib
from time import sleep

from pydantic import EmailStr

from app.config import settings
from app.tasks.celery_app import celery_app
from app.tasks.email_templates import (
    create_booking_confirmation_template,
    create_booking_confirmation_template_for_users_tomorrow,
)


@celery_app.task
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr,
):
    email_to_mok = settings.SMTP_USER_FOR_MAIL
    msg_content = create_booking_confirmation_template(booking, email_to_mok)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg=msg_content)
