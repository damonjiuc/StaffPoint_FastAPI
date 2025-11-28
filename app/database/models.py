from sqlalchemy import Date, func, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    created: Mapped[Date] = mapped_column(Date, default=date.today())
    updated: Mapped[Date] = mapped_column(Date, default=date.today(), onupdate=date.today())