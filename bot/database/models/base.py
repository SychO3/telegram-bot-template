from __future__ import annotations
import datetime
from typing import Annotated

from sqlalchemy import BIGINT, TIMESTAMP, text
from sqlalchemy.orm import DeclarativeBase, mapped_column

int_pk = Annotated[int, mapped_column(primary_key=True, unique=True, autoincrement=False)]
big_int_pk = Annotated[int, mapped_column(primary_key=True, unique=True, autoincrement=False, type_=BIGINT)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("CURRENT_TIMESTAMP"), type_=TIMESTAMP)]


class Base(DeclarativeBase):
    repr_cols_num: int = 3  # print first columns
    repr_cols: tuple[str, ...] = ()  # extra printed columns

    def __repr__(self) -> str:
        cols = [
            f"{col}={getattr(self, col)}"
            for idx, col in enumerate(self.__table__.columns.keys())
            if col in self.repr_cols or idx < self.repr_cols_num
        ]
        return f"<{self.__class__.__name__} {', '.join(cols)}>"
