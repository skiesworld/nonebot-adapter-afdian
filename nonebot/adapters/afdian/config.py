from typing import List, Optional

from pydantic import Field, HttpUrl, BaseModel


class BotInfo(BaseModel):
    user_id: str
    token: Optional[str] = None


class Config(BaseModel):
    afdian_bots: List[BotInfo] = Field(default_factory=list)
    afdian_api_base: HttpUrl = Field("https://afdian.com")
    afdian_hook_secret: str = Field("")
    afdian_enable_hook_bot: bool = Field(False)
