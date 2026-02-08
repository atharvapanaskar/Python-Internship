from sqlalchemy import Column, Integer, String, Text
from database import Base

class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(Text)
    image_url = Column(String(255))
