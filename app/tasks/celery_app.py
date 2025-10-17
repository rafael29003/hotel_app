from celery import Celery
from celery.schedules import crontab

from app.config import settings

celery_app = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=[
        "app.tasks.tasks",
        "app.tasks.scheduled",
    ],
)

celery_app.conf.beat_schedule = {
    "send_message_for_send_email_for_users_tomorrow": {
        "task": "send_message_for_send_email_for_users_tomorrow",
        "schedule": crontab(hour="9", minute="0"),
    },
    "get_email_if_user_comming_3_days": {
        "task": "send_message_for_send_email_for_users_3_days",
        "schedule": crontab(hour="15", minute="30"),
    },
}
