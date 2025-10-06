FROM python:3.11-slim-bullseye

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get clean && \
    apt-get install -y --no-install-recommends \
    build-essential libpq-dev postgresql postgresql-client

RUN pip install --upgrade pip

COPY ./requirements.txt ./requirements.txt
COPY ./entrypoint.sh /entrypoint.sh

# Corrige quebras de linha e dá permissão de execução
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

RUN pip install -r requirements.txt

RUN mkdir -p /django/app
COPY ./app /django/app

WORKDIR /django/app

RUN useradd usertest -m -s /bin/bash && chown -R usertest /home/usertest

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]