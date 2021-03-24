# 异步js渲染服务使用说明
- 安装依赖环境 pip install -r requirements.txt
- 安装pyppeteer pyppeteer-install
- 本地启动命令 python main.py
- 服务器启动命令 uvicorn main:app --reload --host '0.0.0.0' --port 8050
- docker启动命令 docker build -t js_render:v1 . && docker run -d -p 8000:8000 js_render:v1
- api文档访问 http://127.0.0.1:8000/docs