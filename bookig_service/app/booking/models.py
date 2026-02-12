from sqlalchemy import Column, Computed, Date, ForeignKey, Integer
from app.database import Base
from sqlalchemy.orm import relationship

class Bookings(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True) 
    room_id = Column(ForeignKey("rooms.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    total_days = Column(Integer, Computed("date_to - date_from"))
    total_cost = Column(Integer, Computed("(date_to - date_from) * price")) 

    room = relationship("Rooms", back_populates="booking")

    def __str__(self):
        return f"Booking #{self.id}"
    
