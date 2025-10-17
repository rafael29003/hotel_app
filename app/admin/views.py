from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


# Определяем классы админки
class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email, Users.user_to_booking]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = "пользователь"
    name_plural = "пользователи"
    icon = "fa-solid fa-user"


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [
        Bookings.id,
        Bookings.room_id,
        Bookings.user_id,
        Bookings.date_from,
        Bookings.date_to,
        Bookings.price,
        Bookings.total_days,
        Bookings.total_price,
        Bookings.booking_to_user,
        Bookings.booking_to_room,
    ]
    can_delete = False
    can_edit = False
    name = "Бронирование"
    name_plural = "Бронирования"
    icon = "fa-solid fa-calendar-days"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = "__all__"
    name = "Комната"
    name_plural = "Комнаты"
    icon = "fa-solid fa-bed"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = "__all__"
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"
