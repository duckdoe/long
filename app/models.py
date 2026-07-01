import uuid
from datetime import datetime

from sqlalchemy import String, ForeignKey, Boolean, UUID, Text, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Urls(Base):
    __tablename__ = "urls"

    id: Mapped[str] = mapped_column(String(10), primary_key=True)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    has_password: Mapped[bool] = mapped_column(Boolean, default=False)
    clicks_token: Mapped[str] = mapped_column(
        UUID(as_uuid=True), nullable=False, default=uuid.uuid4
    )
    visits: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Passwords(Base):
    __tablename__ = "passwords"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )  # primary key

    url_id: Mapped[str] = mapped_column(
        ForeignKey("urls.id"), nullable=False, unique=True
    )  # url_code fx
    password_hash: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
