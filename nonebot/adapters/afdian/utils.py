import hashlib
import json
import time
from typing import Any, TypeVar

from nonebot.compat import type_validate_python
from nonebot.drivers import Request, Response
from nonebot.utils import logger_wrapper

from .exception import ActionFailed
from .payload import BaseAfdianResponse, WrongResponse

log = logger_wrapper("Afdian")

# 泛型类型，用于根据传入的 response_model 精确推断返回值类型
T = TypeVar("T", bound=BaseAfdianResponse)


def construct_request(
    url: str, user_id: str, token: str, params: dict[str, Any]
) -> Request:
    ts = int(time.time())
    param_json_data = json.dumps(params)
    sign_str = f"{token}params{param_json_data}ts{ts}user_id{user_id}"
    sign = hashlib.md5(sign_str.encode("utf-8")).hexdigest()
    request = Request(
        "POST",
        url=url,
        params={"user_id": user_id, "params": param_json_data, "ts": ts, "sign": sign},
    )
    return request


def parse_response(response: Response, response_model: type[T]) -> T | WrongResponse:
    raw = str(response.content)
    try:
        json_data = json.loads(raw)
    except json.JSONDecodeError as e:
        log("ERROR", f"Response JSON decode failed: {e}; raw={raw[:200]}")
        raise ActionFailed(response) from e

    for model, level in ((response_model, "WARNING"), (WrongResponse, "ERROR")):
        try:
            return type_validate_python(model, json_data)
        except Exception as e:  # 或更窄的 ValidationError
            log(level, f"Failed to parse as {model.__name__}: {e}")

    raise ActionFailed(response)
