from typing import Optional
from xml.dom.minidom import Document
from pydantic import BaseModel
from mongoengine import Document, StringField, IntField, ListField

class User(BaseModel):
    id: Optional[str]
    username: str
    email: str
    password: str


