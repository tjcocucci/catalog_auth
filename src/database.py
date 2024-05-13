from datetime import datetime
import settings

import hashlib
from peewee import *

db = MySQLDatabase(
    "auth",
    user=settings.DATABASE_USER,
    password=settings.DATABASE_PASS,
    host=settings.DATABASE_HOST,
    port=settings.DATABASE_PORT,
)


class User(Model):
    username = CharField(max_length=50, unique=True)
    password = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.now)

    @classmethod
    def create_password(cls, password):
        h = hashlib.md5()
        password = h.update(password.encode("utf-8"))
        return h.hexdigest()

    def __str__(self):
        return self.username

    class Meta:
        database = db
        table_name = "users"
