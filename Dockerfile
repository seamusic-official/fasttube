FROM python:3.11.9

COPY . /server
WORKDIR /server

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["make", "run"]
