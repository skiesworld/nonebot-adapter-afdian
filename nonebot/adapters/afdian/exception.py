from nonebot.drivers import Response
from nonebot.exception import ActionFailed as BaseActionFailed
from nonebot.exception import AdapterException
from nonebot.exception import ApiNotAvailable as BaseApiNotAvailable
from nonebot.exception import NetworkError as BaseNetworkError

from .payload import WrongResponse  # type: ignore


class AfdianAdapterException(AdapterException):
    def __init__(self):
        super().__init__("Afdian")


class NetworkError(BaseNetworkError, AfdianAdapterException):
    def __init__(self, msg: str | None = None):
        super().__init__()
        self.msg: str | None = msg
        """错误原因"""

    def __repr__(self):
        return f"<NetWorkError message={self.msg}>"

    def __str__(self):
        return self.__repr__()


class ActionFailed(
    BaseActionFailed,
    AfdianAdapterException,
):
    def __init__(self, response: Response, wrong: WrongResponse | None = None):
        self.status_code: int = response.status_code
        self.wrong: WrongResponse | None = wrong
        # 兼容 nonebot ActionFailed 预期字段
        if wrong:
            self.code = wrong.ec
            self.message = wrong.em
            # 保留完整结构，便于上层记录
            self.data = wrong.model_dump()
        else:
            self.code = None
            self.message = None
            self.data = None

    def __repr__(self):
        return f"<ActionFailed status={self.status_code} code={self.code} message={self.message}>"

    __str__ = __repr__


class ApiNotAvailable(BaseApiNotAvailable, AfdianAdapterException):
    def __init__(self, msg: str | None = None):
        super().__init__()
        self.msg: str | None = msg
        """错误原因"""
