from pydantic import BaseModel, ConfigDict, EmailStr


class SUser(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str


    model_config = ConfigDict(from_attributes=True)
