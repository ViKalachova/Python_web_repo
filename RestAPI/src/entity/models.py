from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(13), nullable=False)
    birthday: Mapped[str] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(String(250))
