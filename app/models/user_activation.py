from sqlalchemy import Column, ForeignKey, String, Integer, Enum, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class UserActivation(Base):
    __tablename__ = "user_activation"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    acticode = Column(String(255), unique=True, nullable=False)
    expired = Column(DateTime(timezone=True))
    activated_at = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(Enum('activated', 'inactivated'), nullable=False, server_default='inactivated')

    r_user = relationship('User',  backref="user_activation")