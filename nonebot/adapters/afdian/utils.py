import hashlib
import json
import time
from typing import Any

from nonebot.compat import type_validate_python
from nonebot.drivers import Request, Response
from nonebot.utils import logger_wrapper

from .exception import ActionFailed
from .payload import BaseAfdianResponse, WrongResponse

log = logger_wrapper("Afdian")


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


def parse_response(
    response: Response, response_model: type[BaseAfdianResponse]
) -> BaseAfdianResponse | WrongResponse:
    json_data = json.loads(response.content)
    try:
        return type_validate_python(response_model, json_data)
    except Exception as e:
        log("WARNING", f"Failed to parse response as {response_model.__name__}: {e}")
        try:
            # 尝试将响应内容解析为通用的错误响应模型
            return type_validate_python(WrongResponse, json_data)
        except Exception as e:
            log("ERROR", f"Failed to parse response as WrongResponse: {e}")
            raise ActionFailed(response) from e
