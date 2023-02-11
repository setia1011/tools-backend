from sqlalchemy import Column, String, Integer
from app.database import Base


class RefUserIdType(Base):
    __tablename__ = "ref_user_id_type"

    id = Column(Integer, primary_key=True, index=True)
    id_type = Column(String(50), unique=True, nullable=False, index=True)
    id_description = Column(String(225))