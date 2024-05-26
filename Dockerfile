FROM python:3.9

WORKDIR /auth-service

COPY ./requirements.txt /auth-service/requirements.txt

RUN apt-get update
RUN apt-get install gcc default-libmysqlclient-dev -y
RUN apt-get install -y iputils-ping

RUN pip install --no-cache-dir --upgrade -r /auth-service/requirements.txt

COPY ./src /auth-service/src

WORKDIR /auth-service/src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000"]
