FROM python:3.11.9

COPY . /bot
WORKDIR /bot

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir poetry
RUN poetry install

CMD ["make", "run-local"]