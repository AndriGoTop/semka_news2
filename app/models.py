from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped
import datetime


class Base(DeclarativeBase):
    pass


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(primary_key=True)
    heading: Mapped[str] = mapped_column(String())
    article: Mapped[str] = mapped_column(String())
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime())
