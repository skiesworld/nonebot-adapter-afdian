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


def parse_response(response: Response, response_model: type[T]) -> T:
    """解析响应

    成功时返回指定 response_model;
    失败时抛出 ActionFailed, 并在 wrong 字段中附带 WrongResponse。

    :param response: HTTP 响应
    :param response_model: 期望的响应模型类型
    :return: 解析后的响应对象
    """
    raw = str(response.content)
    try:
        json_data = json.loads(raw)
    except json.JSONDecodeError as e:
        log("ERROR", f"Response JSON decode failed: {e}; raw={raw[:200]}")
        raise ActionFailed(response) from e

    # 先尝试解析为正确模型
    try:
        model_obj = type_validate_python(response_model, json_data)
        # 如果 ec != 200, 仍视为业务错误，尝试解析为 WrongResponse 以提供更多调试信息
        if getattr(model_obj, "ec", None) != 200:
            try:
                wrong_obj = type_validate_python(WrongResponse, json_data)
            except Exception:
                wrong_obj = None
            raise ActionFailed(response, wrong=wrong_obj)
        return model_obj
    except Exception as e:
        log("WARNING", f"Failed to parse as {response_model.__name__}: {e}")

    # 尝试解析为 WrongResponse
    try:
        wrong_obj = type_validate_python(WrongResponse, json_data)
        raise ActionFailed(response, wrong=wrong_obj)
    except ActionFailed:
        raise
    except Exception as e:
        log("ERROR", f"Failed to parse as WrongResponse: {e}")
        raise ActionFailed(response) from e
