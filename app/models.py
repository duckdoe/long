import uuid
from datetime import datetime

from sqlalchemy import String, ForeignKey, Boolean, UUID, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.utils import generate_random_code


class Urls(Base):
    __tablename__ = "urls"

    id: Mapped[str] = mapped_column(
        String(10), primary_key=True, default=generate_random_code
    )
    url: Mapped[str] = mapped_column(Text, nullable=False)
    has_password: Mapped[bool] = mapped_column(Boolean, default=False)
    date_created: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Passwords(Base):
    __tablename__ = "passwords"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    password: Mapped[str] = mapped_column(Text, nullable=False)
    url_id: Mapped[str] = mapped_column(ForeignKey("urls.id"), nullable=False)
