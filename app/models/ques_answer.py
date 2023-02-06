from app.database import Base
from sqlalchemy import Column, TEXT, ForeignKey, String, Integer, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class QuesAnswer(Base):
    __tablename__ = 'ques_answer'

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey('ques_question.id'), index=True)
    answer = Column(Integer, ForeignKey('ques_option.id'), index=True)
    
    # ques_question = relationship('QuesQuestion', backref='ques_answer')
    # ques_option = relationship('QuesOption', backref='ques_answer')