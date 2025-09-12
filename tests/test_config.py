from nonebot import get_adapter
from nonebot.adapters.afdian import Adapter  # type: ignore
from nonebot.adapters.afdian.config import BotInfo  # type: ignore


def test_config():
    adapter = get_adapter(Adapter)
    config = adapter.afdian_config  # type: ignore

    # 期望配置中以 token 字段保存
    assert config.afdian_bots == [BotInfo(user_id="fake", token="")]
