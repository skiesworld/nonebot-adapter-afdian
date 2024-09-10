from pathlib import Path

import pytest
from nonebug import NONEBOT_INIT_KWARGS

import nonebot
from nonebot.adapters.afdian.adapter import Adapter

nonebot.adapters.__path__.append(  # type: ignore
    str((Path(__file__).parent.parent / "nonebot" / "adapters").resolve())
)

def pytest_configure(config: pytest.Config) -> None:
    config.stash[NONEBOT_INIT_KWARGS] = {
        "afdian_bots": [
            {
                "user_id": "user_id1",
                "api_token": "api_token1",
            },
        ]
    }

@pytest.fixture(scope="session", autouse=True)
def _init_adapter(nonebug_init: None):
    driver = nonebot.get_driver()
    driver.register_adapter(Adapter)
