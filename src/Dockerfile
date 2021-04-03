
# pull image
FROM python:3.8-buster

# __pycache__ を作らないための設定
ENV PYTHONDONTWRITEBYTECODE 1 
# バイナリレイヤ下での標準出力とエラー出力を抑制
ENV PYTHONUNBUFFERED 1

# django用の設定
ENV APP_HOME=/usr/src/app
RUN mkdir -p $APP_HOME

WORKDIR $APP_HOME

# requirements.txtをAPP_HOMEにコピー
COPY ./requirements.txt .

# インストールを行う
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

