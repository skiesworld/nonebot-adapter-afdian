import asyncio
import hashlib
import json
import time
from functools import partial
from typing import Any, cast

from nonebot import get_plugin_config
from nonebot.adapters import Adapter as BaseAdapter
from nonebot.compat import type_validate_python
from nonebot.drivers import (
    URL,
    Driver,
    Request,
    Response,
    ReverseDriver,
    HTTPServerSetup,
)
from nonebot.utils import escape_tag
from typing_extensions import override

from .bot import Bot
from .config import Config, BotInfo
from .event import OrderNotifyEvent
from .exception import ActionFailed, ApiNotAvailable
from .payload import (
    PingResponse,
    WrongResponse,
    OrderResponse,
    SponsorResponse,
    TSExpiredResponse
)
from .utils import log


class Adapter(BaseAdapter):

    @override
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.afdian_config: Config = get_plugin_config(Config)
        self._setup()

    @classmethod
    @override
    def get_name(cls) -> str:
        return "Afdian"

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
        await asyncio.gather(
            *(self._startup_bot(bot_info) for bot_info in self.afdian_config.afdian_bots)
        )

    async def _startup_bot(self, bot_info: BotInfo):
        bot = Bot(self, self_id=bot_info.user_id, bot_info=bot_info)
        result: PingResponse = await bot.send_ping()
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
            log("ERROR", f"Webhook data parse failed: {e}")
            return Response(400, content='{"ec": 400, "em": "parse event failed"}')
        else:
            if event.ec != 200:
                log("ERROR", f"Webhook data parse failed: {event.em}")
                return Response(400, content='{"ec": 400, "em": "parse event failed"}')
            bot = cast(Bot, self.bots[bot_info.user_id])
            asyncio.create_task(bot.handle_event(event))
        return Response(200, content='{"ec": 200, "em": "success"}')

    @override
    async def _call_api(self, bot: Bot, api: str, **data: Any) -> Any:
        if api not in ("/api/open/ping", "/api/open/query-order", "/api/open/query-sponsor"):
            log("ERROR", f"Unsupported api: {api}")
            raise ApiNotAvailable(api)

        ts = int(time.time())
        param_json_data = json.dumps(data)
        sign_str = f"{bot.api_token}params{param_json_data}ts{ts}user_id{bot.self_id}"
        sign = hashlib.md5(sign_str.encode("utf-8")).hexdigest()
        request = Request(
            "GET",
            URL(self.afdian_config.afdian_api_base + api),
            params={
                "user_id": bot.bot_info.user_id,
                "params": param_json_data,
                "ts": ts,
                "sign": sign
            }
        )
        response = await bot.adapter.request(request)
        response_json = json.loads(response.content)
        for model in (PingResponse, WrongResponse, OrderResponse, SponsorResponse, TSExpiredResponse):
            try:
                result = type_validate_python(model, response_json)
                return result
            except Exception:
                continue
        else:
            log("ERROR", f"Parse result failed: {response_json}")
            raise ActionFailed(response)
