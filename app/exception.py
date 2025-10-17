from fastapi import HTTPException, status


class BookingException(HTTPException):
    """Базовый класс для всех исключений приложения"""

    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class NobookingsException(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "У вас нет бронирований"


class HotelsDateException(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Дата заезда не может быть больше даты выезда"


class HotelsLongException(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Период бронирования не может быть больше 30 дней"


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь с таким email уже существует"


class BookingNotFoundException(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Бронирование не найдено или не принадлежит вам"


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный email или пароль"


class ExpiredTokenException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class RoomIsNotAvailableException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Комната не доступна для бронирования"


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пользователь не найден"
