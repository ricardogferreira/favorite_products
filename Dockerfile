FROM python:3.7-alpine

WORKDIR /opt/workspace
RUN apk add --no-cache --update postgresql-dev build-base python3-dev bash

COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir

COPY wait-for-it.sh /usr/wait-for-it.sh
RUN chmod +x /usr/wait-for-it.sh

COPY . .

RUN chmod +x celery-entrypoint.sh

CMD [ "bash", "app.sh" ]
