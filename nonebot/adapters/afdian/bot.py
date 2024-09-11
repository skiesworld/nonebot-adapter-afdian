from typing_extensions import override
from typing import TYPE_CHECKING, Any, Dict, List, Union

from nonebot.message import handle_event

from nonebot.adapters import Bot as BaseBot

from .event import Event
from .config import BotInfo
from .message import Message, MessageSegment
from .payload import PingResponse, OrderResponse, SponsorResponse, WrongResponse
from .utils import construct_request, parse_response

if TYPE_CHECKING:
    from .adapter import Adapter


class Bot(BaseBot):
    adapter: "Adapter"

    @override
    def __init__(self, adapter: "Adapter", self_id: str, bot_info: BotInfo):
        super().__init__(adapter, self_id)
        self.api_token = bot_info.api_token
        self.bot_info = bot_info

    async def send_ping(self) -> PingResponse | WrongResponse:
        request = construct_request(
            self.adapter.afdian_config.afdian_api_base + "/api/open/ping",
            self.bot_info,
            params={"a": 333}
        )
        response = await self.adapter.request(request)
        return parse_response(response, PingResponse)

    async def __query_order(self, params: Dict[str, Any]) -> OrderResponse | WrongResponse:
        request = construct_request(
            self.adapter.afdian_config.afdian_api_base + "/api/open/query-order",
            self.bot_info,
            params=params
        )
        response = await self.adapter.request(request)
        return parse_response(response, OrderResponse)

    async def query_order_by_page(self, page: int):
        """根据页码查询订单"""
        if page <= 0:
            raise ValueError("page must be greater than 0")
        return await self.__query_order(params={"page": page})

    async def query_order_by_out_trade_no(self, out_trade_no: str):
        """根据订单号查询订单"""
        return await self.__query_order(params={"out_trade_no": out_trade_no})

    async def query_order_by_order_list(self, order_list: List[str]):
        """根据订单号列表查询多个订单"""
        order_list_str = ",".join([out_trade_no for out_trade_no in order_list])
        return await self.__query_order(params={"out_trade_no": order_list_str})

    async def query_sponsor(self, page: int, per_page: int = 20) -> SponsorResponse | WrongResponse:
        """查询赞助者，可选传参每页数量 1-100"""
        if page <= 0:
            raise ValueError("page must be greater than 0")
        if per_page > 100 or per_page < 1:
            raise ValueError("per_page must be between 1 and 100")
        request = construct_request(
            self.adapter.afdian_config.afdian_api_base + "/api/open/query-sponsor",
            self.bot_info,
            params={"page": page, "per_page": per_page}
        )
        response = await self.adapter.request(request)
        return parse_response(response, SponsorResponse)

    async def handle_event(self, event: Event) -> None:
        await handle_event(self, event)

    @override
    async def send(
            self,
            event: Event,
            message: Union[str, Message, MessageSegment],
            **kwargs,
    ) -> Any:
        ...
