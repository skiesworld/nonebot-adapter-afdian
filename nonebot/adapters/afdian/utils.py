import hashlib
import json
import time
from typing import Dict, Any, Type

from nonebot.compat import type_validate_python
from nonebot.drivers import Request, Response
from nonebot.utils import logger_wrapper

from .config import BotInfo
from .exception import ActionFailed
from .payload import WrongResponse, BaseAfdianResponse

log = logger_wrapper("Afdian")


def construct_request(url: str, bot_info: BotInfo, params: Dict[str, Any]) -> Request:
    ts = int(time.time())
    param_json_data = json.dumps(params)
    sign_str = f"{bot_info.api_token}params{param_json_data}ts{ts}user_id{bot_info.user_id}"
    sign = hashlib.md5(sign_str.encode("utf-8")).hexdigest()
    request = Request(
        "POST",
        url=url,
        params={
            "user_id": bot_info.user_id,
            "params": param_json_data,
            "ts": ts,
            "sign": sign
        }
    )
    return request


def parse_response(response: Response, response_model: Type[BaseAfdianResponse]) -> BaseAfdianResponse | WrongResponse:
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
