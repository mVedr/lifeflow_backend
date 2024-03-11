from pydantic import BaseModel


class Message(BaseModel):
    to :str
    subject :str
    body :str
    