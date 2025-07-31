from nonebot import get_adapter
from nonebot.adapters.afdian import Adapter  # type: ignore
from nonebot.adapters.afdian.config import BotInfo  # type: ignore


def test_config():
    adapter = get_adapter(Adapter)
    config = adapter.afdian_config  # type: ignore

    assert config.afdian_bots == [BotInfo(api_token="api_token1", user_id="user_id1")]
