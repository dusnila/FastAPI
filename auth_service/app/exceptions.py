from fastapi import status, HTTPException

class BookingException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class EmailAlreadyExistsException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="пользователь с такой почтой уже зарегестрирован"

class UsernameAlreadyExistsException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="пользователь с таким никнеймом уже зарегестрирован"

class IncorrectEmailorPasswordException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="неверная почта или пароль"

class InvalidLinkException(BookingException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Ссылка недействительна или истек срок действия"

class NotSuchUserExeption(BookingException):
    status_code=status.HTTP_404_NOT_FOUND
    detail="Пользователь с такой почтой отсутвует"

class UserNotToVerifyExeption(BookingException):
    status_code=status.HTTP_403_FORBIDDEN
    detail="Пользователь не был подвержден по почте"

class TokenExpiredException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="токен истек"

class TokenAbsenException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="токен отсутствует"

class TokenNotFoundException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Сессия не найдена или уже была обновлена"

class IncorrectTokenFormatException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="неверный формат токена"

class UserIsNotException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="такой пользовател отсуствует"

class UserIsNotUnathorized(BookingException):
    status_code=status.HTTP_403_FORBIDDEN
    detail="у пользователя недостаточно прав"
