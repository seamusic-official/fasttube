FROM python:3.11.9

COPY . /bot_server
WORKDIR /bot_server

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && pip install --no-cache-dir poetry

RUN poetry install

CMD ["make", "run-local"]