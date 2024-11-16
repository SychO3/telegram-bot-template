from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from bot.database.models.base import Base, big_int_pk, created_at


class LuckyResultModel(Base):
    __tablename__ = "lucky_results"

    period: Mapped[big_int_pk]  # 期号
    created_at: Mapped[created_at]  # 创建时间
    result: Mapped[str] = mapped_column(String(255))  # 开奖结果
