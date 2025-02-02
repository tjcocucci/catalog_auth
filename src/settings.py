import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('../.env'))

SECRET_KEY = os.environ.get("SECRET_KEY")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASS = os.environ.get("DATABASE_PASS")
DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_PORT = int(os.environ.get("DATABASE_PORT_CONTAINER"))
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")
CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS").split(" ")

ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60