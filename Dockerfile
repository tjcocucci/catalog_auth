FROM python:3.9

WORKDIR /auth-service

COPY ./requirements.txt /auth-service/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /auth-service/requirements.txt

COPY ./src /auth-service/src

WORKDIR /auth-service/src

CMD ["uvicorn", "main:app", "--host", "localhost", "--port", "4000"]
