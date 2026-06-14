from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    business_name = Column(String(255), default="")
    business_description = Column(String(1000), default="")
    language = Column(String(10), default="he")
    created_at = Column(DateTime, server_default=func.now())

    contents = relationship("GeneratedContent", back_populates="user", cascade="all, delete-orphan")
