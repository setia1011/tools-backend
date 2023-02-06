from app.database import Base
from sqlalchemy import Column, TEXT, ForeignKey, String, Integer, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class QuesSession(Base):
    __tablename__ = 'ques_session'

    id = Column(Integer, primary_key=True, index=True)
    session = Column(String(500), unique=False, nullable=False, index=True)
    session_description = Column(TEXT)
    