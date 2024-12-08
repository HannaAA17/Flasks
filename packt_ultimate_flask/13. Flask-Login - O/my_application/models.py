from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from flask_login import UserMixin

from .extensions import db


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default='ANY')

    