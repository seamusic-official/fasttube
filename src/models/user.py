from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import Base


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column()
    full_name: Mapped[str] = mapped_column()
    telegram_id: Mapped[str] = mapped_column()
