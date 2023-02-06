from app.database import Base
from sqlalchemy import Column, TEXT, ForeignKey, String, Integer, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class QuesQuestion(Base):
    __tablename__ = 'ques_question'

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey('ques_category.id'), index=True)
    question = Column(String(500), unique=False, nullable=False, index=True)

    ref_category = relationship('QuesCategory', backref='ques_question')
    ref_option = relationship('QuesOption', backref='ques_question')
    ref_answer = relationship('QuesAnswer', backref='ques_question')