from typing import Union, Any, TYPE_CHECKING, Dict, List

from nonebot.message import handle_event
from typing_extensions import override

from nonebot.adapters import Bot as BaseBot

from .config import BotInfo
from .event import Event
from .message import Message, MessageSegment

if TYPE_CHECKING:
    from .adapter import Adapter


class Bot(BaseBot):
    adapter: "Adapter"

    @override
    def __init__(self, adapter: "Adapter", self_id: str, bot_info: BotInfo):
        super().__init__(adapter, self_id)
        self.api_token = bot_info.api_token
        self.bot_info = bot_info

    async def send_ping(self):
        return await self.call_api("/api/open/ping", data={})

    async def __query_order(self, query: Dict[str, Any]):
        return await self.call_api("/api/open/query-order", data=query)

    async def query_order_by_page(self, page: int):
        """根据页码查询订单"""
        if page <= 0:
            raise ValueError("page must be greater than 0")
        return await self.__query_order(query={"page": page})

    async def query_order_by_out_trade_no(self, out_trade_no: str):
        """根据订单号查询订单"""
        return await self.__query_order(query={"out_trade_no": out_trade_no})

    async def query_order_by_order_list(self, order_list: List[str]):
        """根据订单号列表查询多个订单"""
        order_list_str = ",".join([out_trade_no for out_trade_no in order_list])
        return await self.__query_order(query={"out_trade_no": order_list_str})

    async def query_sponsor(self, page: int, per_page: int = 20):
        """查询赞助者，可选传参每页数量 1-100"""
        if page <= 0:
            raise ValueError("page must be greater than 0")
        if per_page > 100 or per_page < 1:
            raise ValueError("per_page must be between 1 and 100")
        return await self.call_api("/api/open/query-sponsor", data={"page": page, "per_page": per_page})

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
