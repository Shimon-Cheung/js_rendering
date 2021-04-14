# -*- coding: utf-8 -*-
"""
@Author ：Shimon-Cheung
@Date   ：2021/03/22 16:39
@Desc   ：基于fastapi高性能的js渲染服务
"""
from fastapi import FastAPI
from pyppeteer import launch
import uvicorn
import asyncio
from pydantic import BaseModel
from starlette.responses import HTMLResponse

app = FastAPI()


# 创建数据模型


class Item(BaseModel):
    url: str
    wait: int


@app.post("/render.html")
async def read_root(item: Item):
    item_dict = item.dict()
    # 使用launch方法调用浏览器，其参数可以传递关键字参数也可以传递字典。
    browser = await launch(
        {
            # 无头模式
            "headless": True,
            # 忽略 Https 报错信息
            "ignoreHTTPSErrors": True,
            # 防止多开导致的假死
            "dumpio": True,
            # 用户目录，用来储存临时缓存
            "userDataDir": "./cache",
            "args": [
                # 关闭掉正在控制的提示
                "--disable-infobars",
                # 设置浏览器窗口最大化
                "--start-maximized",
                # 关闭沙盒模式
                "--no-sandbox",
                # 设置报错等级规避一大堆info信息
                "--log-level=3",
                # 允许跨域
                "--disable-web-security",
                # 进行全局的js渲染，用来解决页面二次跳转
                "--enable-automation"
                # 设置UA请求头
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/85.0.4183.121 Safari/537.36",
                # 添加代理，暂时不开启
                # "--proxy-server=http://127.0.0.1:80"
            ],
            # pyppeteer 异常处理 ValueError: signal only works in main thread
            "handleSIGINT": False,
            "handleSIGTERM": False,
            "handleSIGHUP": False,
        }
    )
    # 打开一个页面
    page = await browser.newPage()
    # 设置页面的大小
    await page.setViewport({"width": 1920, "height": 1080})
    # 开启js渲染
    await page.setJavaScriptEnabled(enabled=True)
    # 进行全局的js渲染，用来解决页面二次跳转
    await page.evaluateOnNewDocument(
        'function(){Object.defineProperty(navigator,"webdriver",{get:()=>undefined})}'
    )
    # 打开链接
    await page.goto(item_dict["url"])
    # 用来等待渲染结果
    await asyncio.sleep(item_dict["wait"])
    page_text = await page.content()  # 页面内容
    await browser.close()
    return HTMLResponse(page_text)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8050)
