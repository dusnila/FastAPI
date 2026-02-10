from pydantic import BaseModel, ConfigDict, EmailStr


class SUserJWT(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)


class SSessionData(BaseModel):
    user_id: int
    refresh_JWT: str

    model_config = ConfigDict(from_attributes=True)    