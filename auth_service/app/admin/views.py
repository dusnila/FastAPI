from sqladmin import ModelView

from app.users.models import User
from app.users.JWT_session.models import Session



class UserAdmin(ModelView, model=User):
    column_list = [c.name for c in User.__table__.c] + [User.sessions]
    name = "пользователи"
    name_plural = "пользователи"
    icon="fa-solid fa-user-gear"



class SessionAdmin(ModelView, model=Session):
    column_list = [c.name for c in Session.__table__.c] + [Session.user_id, Session.user]
    name = "Сессия"
    name_plural = "Сессии"
    icon="fa-solid fa-key"


