# ruff: noqa: TCH001, TCH003, A003, F821
from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from bot.database.models.base import Base, big_int_pk, created_at


class WordModel(Base):
    __tablename__ = "words"

    id: Mapped[big_int_pk] # 用户ID
    word: Mapped[str] # 关键词
    created_at: Mapped[created_at] # 创建时间

    is_push: Mapped[bool] = mapped_column(default=False) # 是否推送
    match_mode: Mapped[str] = mapped_column(default="equal") # 匹配模式