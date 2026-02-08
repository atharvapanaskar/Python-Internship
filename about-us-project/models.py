from sqlalchemy import Column, Integer, String, Text
from database import Base

class AboutUs(Base):
    __tablename__ = "about_us"

    id = Column(Integer, primary_key=True, index=True)
    history = Column(Text)
    objectives = Column(Text)
    achievements = Column(Text)
    core_values = Column(Text)

