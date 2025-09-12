import json
from pathlib import Path

from nonebug import App
import pytest

from nonebot import get_bots


@pytest.mark.asyncio
async def test_webhook_test_order(app: App):
    file_path = Path(__file__).parent / "events.json"

    with open(file_path, encoding="utf-8") as f:  # noqa: ASYNC230
        test_data = json.load(f)
    async with app.test_server() as ctx:
        client = ctx.get_client()
        response = await client.post("/afdian/webhooks/unfake", json=test_data)
        assert response.status_code == 404
        assert "unfake" not in get_bots()
        response = await client.post("/afdian/webhooks/fake", json=test_data)
        assert response.status_code == 200
        assert "fake" in get_bots()
