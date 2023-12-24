from pydantic import BaseModel


class MessageResp(BaseModel):
    message: str = "some message"