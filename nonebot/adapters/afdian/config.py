from typing import List

from pydantic import Field, BaseModel, HttpUrl


class BotInfo(BaseModel):
    user_id: str = ""
    api_token: str = ""


class Config(BaseModel):
    afdian_bots: List[BotInfo] = Field(default=[])
    afdian_api_base: HttpUrl = Field("https://afdian.com")
