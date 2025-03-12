from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, DateTime, func
from datetime import datetime

from src.database import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    num_guests: Mapped[int] = mapped_column(Integer)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE", onupdate="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    users: Mapped["User"] = relationship(back_populates="reservations")
    events: Mapped["Event"] = relationship(back_populates="reservations")
