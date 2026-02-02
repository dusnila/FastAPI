from pydantic import BaseModel, ConfigDict, EmailStr

class SUserAuth(BaseModel):
    username : str
    email : EmailStr
    password : str

    model_config = ConfigDict(from_attributes=True)


class SUserRegister(BaseModel):
    username : str
    email : EmailStr
    password : str


    model_config = ConfigDict(from_attributes=True)


class SSendMessageEmail(BaseModel):
    email : EmailStr

    model_config = ConfigDict(from_attributes=True)


class SUserJWT(BaseModel):
    username: str
    email: EmailStr
    refresh_JWT: str

    model_config = ConfigDict(from_attributes=True)