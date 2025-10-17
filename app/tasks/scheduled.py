from asgiref.sync import async_to_sync

from app.tasks.celery_app import celery_app
from app.tasks.dao import SendDao
from app.tasks.tasks import send_booking_confirmation_email


async def get_email_if_user_comming_tomorrow():
    days = 1
    users_and_bookings = await SendDao.users_bookings_for_tomorrow(days=days)
    for user in users_and_bookings:
        user_email_and_booking_dict = dict(user)
        send_booking_confirmation_email(
            user_email_and_booking_dict, user_email_and_booking_dict["email"]
        )


@celery_app.task(name="send_message_for_send_email_for_users_tomorrow")
def send_message_for_send_email_for_users_tomorrow():
    async_to_sync(get_email_if_user_comming_tomorrow)()


async def get_email_if_user_comming_3_days():
    days = 3
    users_and_bookings = await SendDao.users_bookings_for_tomorrow(days=days)
    for user in users_and_bookings:
        user_email_and_booking_dict = dict(user)
        send_booking_confirmation_email(
            user_email_and_booking_dict, user_email_and_booking_dict["email"]
        )


@celery_app.task(name="send_message_for_send_email_for_users_3_days")
def send_message_for_send_email_for_users_3_days():
    async_to_sync(get_email_if_user_comming_3_days)()
