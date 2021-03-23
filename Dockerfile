FROM python:latest

COPY main.py main.py

COPY requirements.txt requirements.txt

RUN pip install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt

RUN pyppeteer-install

EXPOSE 8000

CMD uvicorn main:app --reload --host '0.0.0.0'