# -*- coding: utf-8 -*-
"""
@Author ：Shimon-Cheung
@Date   ：2020/9/30 11:29
@Desc   ：基于fastapi高性能的js渲染服务
"""
from fastapi import FastAPI
from pyppeteer import launch
import uvicorn
import asyncio
from pydantic import BaseModel

app = FastAPI()


# 创建数据模型
class Item(BaseModel):
    url: str
    wait: int


@app.post("/")
async def read_root(item: Item):
    item_dict = item.dict()
    # 使用launch方法调用浏览器，其参数可以传递关键字参数也可以传递字典。
    browser = await launch(
        {
            # 无头模式
            'headless': True,
            # 忽略 Https 报错信息
            'ignoreHTTPSErrors': True,
            # 防止多开导致的假死
            'dumpio': True,
            # 用户目录，用来储存临时缓存
            'userDataDir': "./cache",
            'args': [
                # 关闭掉正在控制的提示
                '--disable-infobars',
                # 设置浏览器窗口最大化
                '--start-maximized',
                # 关闭沙盒模式
                '--no-sandbox',
                # 设置UA请求头
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
                # 添加代理，暂时不开启
                # "--proxy-server=http://127.0.0.1:80"
            ]
        }
    )
    # 打开一个页面
    page = await browser.newPage()
    await page.setViewport({'width': 1920, 'height': 1080})  # 设置页面的大小
    await page.setJavaScriptEnabled(enabled=True)  # 开启js渲染
    # 打开链接
    await page.goto(item_dict["url"])
    # 用来等待渲染结果
    await asyncio.sleep(item_dict["wait"])
    page_text = await page.content()  # 页面内容
    await browser.close()
    return {"data": page_text}


if __name__ == '__main__':
    uvicorn.run(app)
