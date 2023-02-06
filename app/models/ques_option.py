from app.database import Base
from sqlalchemy import Column, TEXT, ForeignKey, String, Integer, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class QuesOption(Base):
    __tablename__ = 'ques_option'

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey('ques_question.id'), index=True)
    option = Column(String(500), unique=False, nullable=False, index=True)
    
    # ques_question = relationship('QuesQuestion', backref='ques_option')