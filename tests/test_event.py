import json
from pathlib import Path

import pytest

from nonebot.adapters.afdian.event import OrderNotifyEvent  # type: ignore
from nonebot.compat import type_validate_python


@pytest.mark.asyncio
async def test_event():
    with (Path(__file__).parent / "events.json").open("r") as f:
        test_event = json.load(f)

    parsed = type_validate_python(OrderNotifyEvent, test_event)
    assert isinstance(parsed, OrderNotifyEvent)
