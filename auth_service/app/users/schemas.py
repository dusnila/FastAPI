from pydantic import BaseModel, ConfigDict, EmailStr

class SUserAuth(BaseModel):
    username : str
    email : EmailStr
    password : str

    model_config = ConfigDict(from_attributes=True)


class SUser(BaseModel):
    id : int
    username : str
    email : EmailStr
    hashed_password: str
    role: str
    is_active : bool

    model_config = ConfigDict(from_attributes=True)


class SSendMessageEmail(BaseModel):
    email : EmailStr

    model_config = ConfigDict(from_attributes=True)
