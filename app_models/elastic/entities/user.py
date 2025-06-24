from pydantic import BaseModel


class UserMin(BaseModel):
    uuid: str
    fullname: str
    email: str
