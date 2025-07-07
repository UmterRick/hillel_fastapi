from typing import Union

from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

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


class UserAddressRead(BaseModel):
    id: int
    title: Optional[str]
    city: str
    street: str
    house: str
    apartment: Optional[str]
    post_code: Optional[str]
    additional_info: Optional[str]

    model_config = ConfigDict(from_attributes=True)