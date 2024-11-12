from __future__ import annotations
import csv
import io
from datetime import datetime, timedelta, timezone

from aiogram.types import BufferedInputFile

from bot.database.models import UserModel

CHINA_TZ = timezone(timedelta(hours=8))


async def convert_users_to_csv(users: list[UserModel]) -> BufferedInputFile:
    """Export all users in csv file."""
    columns = UserModel.__table__.columns.keys()
    data = [[getattr(user, column) for column in columns] for user in users]

    s = io.StringIO()
    writer = csv.writer(s)
    writer.writerow(columns)
    writer.writerows(data)
    s.seek(0)

    return BufferedInputFile(
        file=s.getvalue().encode("utf-8"),
        filename=f"users_{datetime.now(CHINA_TZ).strftime('%Y.%m.%d_%H.%M')}.csv",
    )
