from pydantic import BaseModel


class JsonObject(BaseModel):
    name: str | None = None
    value: int | None = None
