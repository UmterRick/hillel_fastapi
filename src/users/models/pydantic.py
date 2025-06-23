from typing import Union

from pydantic import BaseModel, EmailStr, ConfigDict

class UserModel(BaseModel):
    id: Union[int, None]
    first_name:str
    last_name:str
    email: EmailStr
    phone_number: str
    is_active: bool | None

    model_config = ConfigDict(from_attributes=True)


class UserWithPassword(UserModel):
    hashed_password: str