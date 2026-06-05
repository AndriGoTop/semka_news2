from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped
from typing import Optional
from sqlalchemy.orm import relationship
import datetime


class Base(DeclarativeBase):
    pass


class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    heading: Mapped[str] = mapped_column(String(30))
    article: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime())

