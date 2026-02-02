from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Session(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer ,ForeignKey("users.id"), nullable=False)
    refresh_JWT = Column(String, nullable=False, unique=True)
    
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("Users", back_populates="sessions")