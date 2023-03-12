FROM python:3.8.2-alpine

LABEL maintainer="chchchuang <chchchuang@gmail.com>"

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

COPY . /twittor

WORKDIR /twittor

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt && pip install gunicorn && chmod 755 run_server.sh

RUN flask db upgrade

EXPOSE 8000

ENTRYPOINT ["./run_server.sh"]

