from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class GeneratedContent(Base):
    __tablename__ = "generated_contents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    prompt_data = Column(Text, nullable=False)
    generated_text = Column(Text, nullable=False)
    language = Column(String(10), default="he")
    platform = Column(String(50), default="")
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="contents")
