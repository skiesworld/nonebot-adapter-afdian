from typing import Any

from pydantic import BaseModel, Field


class Request(BaseModel):
    """Request Data"""

    user_id: str
    params: str
    ts: int
    sign: str


class KVString(BaseModel):
    """KV String Data"""

    kv_string: str


class WrongResponseData(BaseModel):
    """错误响应"""

    explain: str
    debug: KVString
    request: Request


class TSExpiredResponseData(BaseModel):
    """TS 过期"""

    explain: str


class PingResponseData(BaseModel):
    """Ping Response Data"""

    uid: str
    request: Request


class ResponseData(BaseModel):
    """Response Data"""

    total_count: int | None = None
    total_page: int | None = None
    request: Request


class BaseAfdianResponse(BaseModel):
    """Base Afdian Response"""

    ec: int
    em: str


class WrongResponse(BaseAfdianResponse):
    """请求错误"""

    data: WrongResponseData


class PingResponse(BaseAfdianResponse):
    """Ping 回应"""

    data: PingResponseData


class TSExpiredResponse(BaseAfdianResponse):
    """TS 过期"""

    data: TSExpiredResponseData


class SkuDetail(BaseModel):
    """售卖类型"""

    sku_id: str
    count: int
    name: str
    album_id: str | None = None
    pic: str | None = None
    stock: str | None = None
    post_id: str | None = None


class Order(BaseModel):
    """Order Model"""

    out_trade_no: str
    """订单号"""
    custom_order_id: str | None = None
    """自定义信息"""
    plan_title: str | None = None
    """Hook消息中可能不存在"""
    create_time: int | None = None
    """Hook消息中可能不存在"""
    user_private_id: str | None = None
    user_id: str
    """下单用户ID"""
    plan_id: str
    """方案ID，如自选，则为空"""
    title: str | None = None
    """方案描述"""
    month: int
    """赞助月份"""
    total_amount: str
    """真实付款金额，如有兑换码，则为 0.00"""
    show_amount: str
    """显示金额，如有折扣则为折扣前金额"""
    status: int
    """2 为交易成功。目前仅会推送此类型"""
    remark: str | None = None
    """订单留言"""
    redeem_id: str | None = None
    """兑换码ID"""
    product_type: int
    """0 表示常规方案，1 表示售卖方案"""
    discount: str | None = None
    """折扣"""
    sku_detail: list[SkuDetail] | None = None
    """如果为售卖类型，以数组形式表示具体型号"""
    address_person: str | None = None
    """收件人"""
    address_phone: str | None = None
    """收件人电话"""
    address_address: str | None = None
    """收件人地址"""


class WebhookData(BaseModel):
    """Webhook Data"""

    type: str | None = None
    order: Order


class OrderResponseData(ResponseData):
    """订单响应"""

    list: list[Order]


class OrderResponse(BaseAfdianResponse):
    """订单 Response"""

    data: OrderResponseData


class SponsorPlan(BaseModel):
    """赞助方案"""

    plan_id: str
    rank: int
    user_id: str
    status: int
    name: str
    pic: str
    desc: str
    price: str
    update_time: int
    pay_month: int
    show_price: str
    independent: int
    permanent: int
    can_buy_hide: int
    need_address: int
    product_type: int
    sale_limit_count: int
    need_invite_code: bool
    expire_time: int
    sku_processed: list
    rankType: int


class Timing(BaseModel):
    timing_on: int
    timing_off: int


class CurrentPlan(BaseModel):
    """赞助方案"""

    can_ali_agreement: int | None = None
    plan_id: str | None = None
    rank: int | None = None
    user_id: str | None = None
    status: int | None = None
    name: str
    pic: str | None = None
    desc: str | None = None
    price: str | None = None
    update_time: int | None = None
    timing: Timing | None = None
    pay_month: int | None = None
    show_price: str | None = None
    show_price_after_adjust: str | None = None
    has_coupon: int | None = None
    coupon: list | None = None
    favorable_price: int | None = None
    independent: int | None = None
    permanent: int | None = None
    can_buy_hide: int | None = None
    need_address: int | None = None
    product_type: int | None = None
    sale_limit_count: int | None = None
    need_invite_code: bool | None = None
    bundle_stock: int | None = None
    bundle_sku_select_count: int | None = None
    config: dict[str, Any] | None = None
    has_plan_config: int | None = None
    shipping_fee_info: list | None = None
    expire_time: int | None = None
    sku_processed: list | None = None
    rank_type: int | None = Field(None, alias="rankType")


class User(BaseModel):
    """用户属性"""

    user_id: str
    """用户唯一ID"""
    name: str
    """昵称，非唯一，可重复"""
    avatar: str
    """头像"""


class SponsorList(BaseModel):
    """赞助者列表"""

    sponsor_plans: list[SponsorPlan]
    """赞助方案"""
    current_plan: CurrentPlan
    """当前赞助方案，如果节点仅有 name: ""，不包含其它内容时，表示无方案"""
    all_sum_amount: str
    """累计赞助金额，此处为折扣前金额。如有兑换码，则此处为虚拟金额，回比实际提现的多"""
    create_time: int | None = None
    """int 秒级时间戳，表示成为赞助者的时间，即首次赞助时间"""
    first_pay_time: int | None = None
    last_pay_time: int
    """int 秒级时间戳，最近一次赞助时间"""
    user: User
    """用户属性"""


class SponsorResponseData(ResponseData):
    """赞助者响应数据"""

    list: list[SponsorList]


class SponsorResponse(BaseAfdianResponse):
    """赞助者 Response"""

    data: SponsorResponseData
