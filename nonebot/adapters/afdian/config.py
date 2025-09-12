from pydantic import BaseModel, Field


class BotInfo(BaseModel):
    user_id: str
    token: str | None = None


class Config(BaseModel):
    afdian_bots: list[BotInfo] = Field(default_factory=list)
    afdian_api_base: str = Field("https://afdian.com")
    afdian_hook_secret: str = Field("")
