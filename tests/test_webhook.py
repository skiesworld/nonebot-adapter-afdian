import json

from nonebug import App
import pytest

from nonebot import logger
from nonebot.adapters.afdian import OrderNotifyEvent  # type: ignore
from nonebot.compat import type_validate_python


@pytest.mark.asyncio
async def test_webhook_test_order(app: App):
    test_data = """{
        "ec": 200,
        "em": "ok",
        "data": {
            "type": "order",
            "order": {
                "out_trade_no": "202106232138371083454010626",
                "user_id": "adf397fe8374811eaacee52540025c377",
                "plan_id": "a45353328af911eb973052540025c377",
                "month": 1,
                "total_amount": "5.00",
                "show_amount": "5.00",
                "status": 2,
                "remark": "",
                "redeem_id": "",
                "product_type": 0,
                "discount": "0.00",
                "sku_detail": [],
                "address_person": "",
                "address_phone": "",
                "address_address": ""
            }
        }
    }
    """

    event = type_validate_python(OrderNotifyEvent, json.loads(test_data))
    logger.info(event)

    async with app.test_server() as ctx:
        client = ctx.get_client()
        response = await client.post("/afdian/webhooks/user_id1", json=test_data)
        logger.info(f"Response: {response.status_code}, {response.json()}")
        assert response.content == "test"
        # assert response.json() == {"status": "success"}
        # assert "fake" in nonebot.get_bots()
