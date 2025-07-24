from nonebot.drivers import Response
from nonebot.exception import ActionFailed as BaseActionFailed
from nonebot.exception import AdapterException
from nonebot.exception import ApiNotAvailable as BaseApiNotAvailable
from nonebot.exception import NetworkError as BaseNetworkError


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
    def __init__(self, response: Response):
        self.status_code: int = response.status_code
        self.code: int | None = None
        self.message: str | None = None
        self.data: dict | None = None


class ApiNotAvailable(BaseApiNotAvailable, AfdianAdapterException):
    def __init__(self, msg: str | None = None):
        super().__init__()
        self.msg: str | None = msg
        """错误原因"""
