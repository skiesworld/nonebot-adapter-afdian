from nonebot import escape_tag, model_dump
from nonebot.adapters import Event as BaseEvent
from typing_extensions import override

from .message import Message
from .payload import WebhookData


class Event(BaseEvent):
    """Event"""
    ec: int
    em: str

    @override
    def get_type(self) -> str:
        raise ValueError("Event has no type")

    @override
    def get_event_name(self) -> str:
        raise ValueError("Event has no name")

    @override
    def get_event_description(self) -> str:
        return escape_tag(str(model_dump(self)))

    @override
    def get_message(self) -> Message:
        raise ValueError("Event has no context")

    @override
    def get_plaintext(self) -> str:
        raise ValueError("Event has no plaintext")

    @override
    def get_user_id(self) -> str:
        raise ValueError("Event has no sender")

    @override
    def get_session_id(self) -> str:
        raise ValueError("Event has no sender")

    @override
    def is_tome(self) -> bool:
        return False


class OrderNotifyEvent(Event):
    """Order Notify Event"""
    data: WebhookData

    @override
    def get_type(self) -> str:
        return "notice"

    @override
    def get_event_name(self) -> str:
        return "order_notify"

    @override
    def get_user_id(self) -> str:
        return self.data.order.user_private_id

    @override
    def get_session_id(self) -> str:
        return self.data.order.user_private_id

    @override
    def get_event_description(self) -> str:
        return f"Order {self.data.order.out_trade_no} from user @{self.data.order.user_private_id}"
