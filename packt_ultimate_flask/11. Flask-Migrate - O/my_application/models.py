from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .extensions import db


class Member(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(50))
    # subscribed: Mapped[Optional[bool]]


class Order(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    total: Mapped[Optional[int]]
