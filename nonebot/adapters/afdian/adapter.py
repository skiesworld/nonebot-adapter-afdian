import json
import asyncio
from typing import Any, cast
from functools import partial
from typing_extensions import override

from nonebot.utils import escape_tag
from nonebot.compat import type_validate_python
from nonebot.drivers import (
    URL,
    Driver,
    Request,
    Response,
    ReverseDriver,
    HTTPServerSetup,
)

from nonebot import get_plugin_config
from nonebot.adapters import Adapter as BaseAdapter
from nonebot.adapters.afdian.exception import ApiNotAvailable

from .bot import Bot
from .config import Config, BotInfo
from .event import OrderNotifyEvent
from .utils import log, parse_response, construct_request
from .payload import PingResponse, OrderResponse, WrongResponse


class Adapter(BaseAdapter):

    @override
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.afdian_config: Config = get_plugin_config(Config)
        self.tasks: list[asyncio.Task] = []
        self._setup()

    @classmethod
    @override
    def get_name(cls) -> str:
        return "AFDian"

    def _setup(self):
        if not isinstance(self.driver, ReverseDriver):
            log(
                "WARNING",
                f"Current driver {self.config.driver} is not a ReverseDriver. {self.get_name()}"
                " Webhook disabled.",
            )
        for bot_info in self.afdian_config.afdian_bots:
            webhook_route = HTTPServerSetup(
                URL("/afdian/webhooks/" + bot_info.user_id),
                "POST",
                self.get_name(),
                partial(self._handle_webhook, bot_info=bot_info),
            )
            self.setup_http_server(webhook_route)
        self.driver.on_startup(self._startup)

    async def _startup(self):
        for bot_info in self.afdian_config.afdian_bots:
            self.tasks.append(asyncio.create_task(self._startup_bot(bot_info)))

    async def _startup_bot(self, bot_info: BotInfo):
        bot = Bot(self, self_id=bot_info.user_id, bot_info=bot_info)
        request = construct_request(
            self.afdian_config.afdian_api_base + "/api/open/ping",
            bot_info,
            params={"a": 333}
        )
        response = await self.request(request)
        result = parse_response(response, PingResponse)

        if isinstance(result, WrongResponse):
            log(
                "ERROR",
                f"<y>Bot {bot.self_id}</y> connect <r>failed</r>, explain: {result.data.explain}, debug: {result.data.debug.kv_string}"
            )
            return

        if result.ec != 200:
            log("ERROR", f"<y>Bot {bot.self_id}</y> connect <r>failed</r>")
            return
        self.bot_connect(bot)
        log("INFO", f"<y>Bot {escape_tag(bot_info.user_id)}</y> connected")

    async def _handle_webhook(self, request: Request, bot_info: BotInfo) -> Response:
        json_data = json.loads(request.content)
        try:
            event = type_validate_python(OrderNotifyEvent, json_data)
        except Exception as e:
            log("ERROR", f"Webhook data parse to event failed: {e}")
            return Response(400, content='{"ec": 400, "em": "parse data failed"}')

        # 每当有订单时，平台会请求开发者配置的url（如果服务器异常，可能不保证能及时推送，因此建议结合API一起使用）
        verify_request = construct_request(
            self.afdian_config.afdian_api_base + "/api/open/query-order",
            bot_info,
            {"out_trade_no": event.data.order.out_trade_no}
        )
        verify_response: Response = await self.request(verify_request)

        # 请求失败
        if verify_response.status_code != 200:
            log("ERROR", f"Webhook data request failed when verify: {verify_response.content}")
            return Response(400, content='{"ec": 400, "em": "Webhook data request failed when verify"}')

        verify_order: OrderResponse | WrongResponse = parse_response(verify_response, OrderResponse)
        if isinstance(verify_request, WrongResponse):
            log("ERROR", f"Webhook data request failed when verify, ec: {verify_request.ec}, em: {verify_request.em}")
            return Response(400, content='{"ec": 400, "em": "Webhook data request failed when verify"}')
        else:
            # 订单列表为空
            if not verify_order.data.list:
                log("ERROR", "Webhook data <y>list</y> is <r>empty</r>! Verify failed.")
                return Response(400, content='{"ec": 400, "em": "order list is empty"}')

            # 订单列表不为空但不一定有需要的数据
            for order in verify_order.data.list:
                if order.out_trade_no == event.data.order.out_trade_no:
                    bot = cast(Bot, self.bots[bot_info.user_id])
                    asyncio.create_task(bot.handle_event(event))
                    return Response(200, content='{"ec": 200, "em": "success"}')
            else:
                log("ERROR", "Webhook data <y>out_trade_no</y> not found in <y>list</y>! Verify failed.")
                return Response(400, content='{"ec": 400, "em": "order not found when verify"}')

    @override
    async def _call_api(self, bot: Bot, api: str, **data: Any) -> Any:
        if api not in ("/api/open/ping", "/api/open/query-order", "/api/open/query-sponsor"):
            log("ERROR", f"Unsupported api: {api}")
            raise ApiNotAvailable(api)
