from nonebot.drivers import Response
from nonebot.utils import logger_wrapper
from nonebot.compat import type_validate_python

from nonebot.adapters.afdian.payload import (
    PingResponse,
    OrderResponse,
    WrongResponse,
    SponsorResponse,
    TSExpiredResponse,
)

log = logger_wrapper("Afdian")


def verify_model(response: Response):
    for model in (PingResponse, WrongResponse, OrderResponse, SponsorResponse, TSExpiredResponse):
        try:
            result = type_validate_python(model, response.content)
            return result
        except Exception:
            continue
    else:
        log.error("未知的返回数据")
        return None
