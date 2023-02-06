from app.database import Base
from sqlalchemy import Column, TEXT, ForeignKey, String, Integer, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class QuesCategory(Base):
    __tablename__ = "ques_category"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(255), unique=False, nullable=False, index=True)
    category_description = Column(TEXT)