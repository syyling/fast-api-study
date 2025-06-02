from pydantic.main import BaseModel


class CreateToDoRequest(BaseModel):
    contents: str
    is_done: bool