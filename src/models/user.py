from sqlalchemy.orm import Mapped
from models.base import Base


class User(Base):
    __tablename__ = "users"

    username: Mapped[str]
    telegram_id: Mapped[str]
