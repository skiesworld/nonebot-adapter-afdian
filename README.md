# nonebot-adapter-afdian

基于 NoneBot2 的爱发电适配器

## 使用

1.  安装
    ```shell
    pip install nonebot-adapter-afdian
    ```

2.  启用
    ```toml
    adapters = [
        { name = "Afdian", module_name = "nonebot.adapter.afdian" }
    ]
    ```

3.  配置
    ```dotenv
    AFDIAN_BOTS='[
        {
            "user_id": "Your User id",
            "api_token": "Your Api Token"
        }
    ]'
    ```

## API

```python
from nonebot import on_notice
from nonebot.adapters.afdian import OrderNotifyEvent, Bot

test_afd = on_notice()


@test_afd.handle()
async def handle_afd(bot: Bot, event: OrderNotifyEvent):
    result1 = await bot.query_order_by_page(page=1)
    print(result1)

    result2 = await bot.query_order_by_out_trade_no(
        out_trade_no="202408070218485652995332024"
        )
    print(result2)

    result3 = await bot.query_order_by_order_list(
        order_list=["202408070218485652995332024", "202308281533159897535713113"]
        )
    print(result3)

    result4 = await bot.query_sponsor(page=1)
    print(result4)

    result5 = await bot.query_sponsor(page=1, per_page=20) # 查询第一页，每页20个
    print(result5)
```

## 特别感谢

- [NoneBot2](https://github.com/nonebot/nonebot2)：开发框架。

## 贡献与支持

觉得好用可以给这个项目点个 `Star` 或者去 [爱发电](https://afdian.net/a/17TheWord) 投喂我。

有意见或者建议也欢迎提交 [Issues](https://github.com/MineGraphCN/nonebot-adapter-afdian/issues)
和 [Pull requests](https://github.com/MineGraphCN/nonebot-adapter-afdian/pulls) 。

## 开源许可

本项目使用 [MIT](./LICENSE) 作为开源许可证。

