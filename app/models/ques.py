from app.database import Base
from sqlalchemy import Column, TEXT, ForeignKey, String, Integer, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Ques(Base):
    __tablename__ = 'ques'

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey('ques_session.id'), index=True)
    question_id = Column(Integer, ForeignKey('ques_question.id'), index=True)
    question_status = Column(Enum('enabled', 'disabled'), nullable=False, server_default='enabled')

    ref_session = relationship('QuesSession', backref='ques')
    ref_question = relationship('QuesQuestion', backref='ques')