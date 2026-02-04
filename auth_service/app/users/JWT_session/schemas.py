from pydantic import BaseModel, ConfigDict, EmailStr


class SUserJWT(BaseModel):
    username: str
    email: EmailStr
    refresh_JWT: str

    model_config = ConfigDict(from_attributes=True)


class SSession(BaseModel):
    user_id: int
    refresh_JWT: str

    model_config = ConfigDict(from_attributes=True)    