from fastapi import status, HTTPException

class BookingException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserAlredyExistsException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="пользователь уже зарегестрирован"

class IncorrectEmailorPasswordException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="неверная почта или пароль"

class TokenExpiredException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="токен истек"

class TokenAbsenException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="токен отсутствует"

class IncorrectTokenFormatException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="неверный формат токена"

class UserIsNotException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED

class RoomCannotBeBooked(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="не осталось свободных мест"

