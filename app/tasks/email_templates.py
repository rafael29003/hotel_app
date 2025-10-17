from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def create_booking_confirmation_template(
    booking: dict,
    email_to: EmailStr,
):
    email = EmailMessage()
    email["Subject"] = "Подтверждение бронирования"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
        <h1>Бронирование комнаты</h1>
        <p>Вы забронировали комнату</p>
        <p>Дата заезда: {booking["date_from"]}</p>
        <p>Дата выезда: {booking["date_to"]}</p>
        <p>Количество ночей: {booking["total_days"]}</p>
        <p>Цена за ночь: {booking["price"]}</p>
        <p>Общая цена: {booking["total_price"]}</p>
        """,
        subtype="html",
    )

    return email


def create_booking_confirmation_template_for_users_tomorrow(
    info_user_and_booking: dict,
):
    email = EmailMessage()
    email["Subject"] = "Напоминание о бронировании"
    email["From"] = settings.SMTP_USER
    email["To"] = info_user_and_booking["email"]

    email.set_content(
        f"""
        <h1>Напоминание о бронировании</h1>
        <p>Вы забронировали комнату</p>
        <p>Дата заезда: {info_user_and_booking['date_from']}</p>
        <p>Дата выезда: {info_user_and_booking['date_to']}</p>
        <p>Количество ночей: {info_user_and_booking['total_days']}</p>
        <p>Цена за ночь: {info_user_and_booking['price']}</p>
        <p>Общая цена: {info_user_and_booking['total_price']}</p>
        """,
        subtype="html",
    )
    return email
