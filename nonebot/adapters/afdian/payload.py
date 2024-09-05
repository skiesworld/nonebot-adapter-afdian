from typing import Optional, List, Any, Dict

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

    total_count: Optional[int] = None
    total_page: Optional[int] = None
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


class SKUDetail(BaseModel):
    """售卖类型"""

    sku_id: str
    count: int
    name: str
    album_id: Optional[str] = ""
    pic: Optional[str] = ""
    stock: Optional[str] = ""
    post_id: Optional[str] = ""


class Order(BaseModel):
    """Order Model"""

    out_trade_no: str
    """订单号"""
    custom_order_id: Optional[str] = None
    """自定义信息"""
    plan_title: str
    user_private_id: str
    user_id: str
    """下单用户ID"""
    plan_id: str
    """方案ID，如自选，则为空"""
    title: Optional[str] = ""
    """方案描述"""
    month: int
    """赞助月份"""
    total_amount: str
    """真实付款金额，如有兑换码，则为 0.00"""
    show_amount: str
    """显示金额，如有折扣则为折扣前金额"""
    status: int
    """2 为交易成功。目前仅会推送此类型"""
    remark: Optional[str] = ""
    """订单留言"""
    redeem_id: Optional[str] = ""
    """兑换码ID"""
    product_type: int
    """0 表示常规方案，1 表示售卖方案"""
    discount: Optional[str] = ""
    """折扣"""
    sku_detail: Optional[List[SKUDetail]] = []
    """如果为售卖类型，以数组形式表示具体型号"""
    address_person: Optional[str] = ""
    """收件人"""
    address_phone: Optional[str] = ""
    """收件人电话"""
    address_address: Optional[str] = ""
    """收件人地址"""


class WebhookData(BaseModel):
    """Webhook Data"""

    type: Optional[str] = None
    order: Order


class OrderResponseData(ResponseData):
    """订单响应"""

    list: List[Order]


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
    sku_processed: List
    rankType: int


class Timing(BaseModel):
    timing_on: int
    timing_off: int


class CurrentPlan(BaseModel):
    """赞助方案"""

    can_ali_agreement: Optional[int] = None
    plan_id: Optional[str] = None
    rank: Optional[int] = None
    user_id: Optional[str] = None
    status: Optional[int] = None
    name: str
    pic: Optional[str] = None
    desc: Optional[str] = None
    price: Optional[str] = None
    update_time: Optional[int] = None
    timing: Optional[Timing] = None
    pay_month: Optional[int] = None
    show_price: Optional[str] = None
    show_price_after_adjust: Optional[str] = None
    has_coupon: Optional[int] = None
    coupon: Optional[List] = None
    favorable_price: Optional[int] = None
    independent: Optional[int] = None
    permanent: Optional[int] = None
    can_buy_hide: Optional[int] = None
    need_address: Optional[int] = None
    product_type: Optional[int] = None
    sale_limit_count: Optional[int] = None
    need_invite_code: Optional[bool] = None
    bundle_stock: Optional[int] = None
    bundle_sku_select_count: Optional[int] = None
    config: Optional[Dict[str, Any]] = None
    has_plan_config: Optional[int] = None
    shipping_fee_info: Optional[List] = None
    expire_time: Optional[int] = None
    sku_processed: Optional[List] = None
    rank_type: Optional[int] = Field(None, alias='rankType')


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

    sponsor_plans: List[SponsorPlan]
    """赞助方案"""
    current_plan: CurrentPlan
    """当前赞助方案，如果节点仅有 name: ""，不包含其它内容时，表示无方案"""
    all_sum_amount: str
    """累计赞助金额，此处为折扣前金额。如有兑换码，则此处为虚拟金额，回比实际提现的多"""
    create_time: Optional[int] = None
    """int 秒级时间戳，表示成为赞助者的时间，即首次赞助时间"""
    first_pay_time: Optional[int] = None
    last_pay_time: int
    """int 秒级时间戳，最近一次赞助时间"""
    user: User
    """用户属性"""


class SponsorResponseData(ResponseData):
    """赞助者响应数据"""

    list: List[SponsorList]


class SponsorResponse(BaseAfdianResponse):
    """赞助者 Response"""

    data: SponsorResponseData
