from pydantic import BaseModel
from typing import Optional


class GroupBase(BaseModel):
    name: str


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int

    class Config:
        from_attributes = True


class PersonBase(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    group_id: Optional[int] = None


class PersonCreate(PersonBase):
    pass


class Person(PersonBase):
    id: int

    class Config:
        from_attributes = True