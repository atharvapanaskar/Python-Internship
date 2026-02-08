from sqlalchemy import Column, Integer, String, Text
from database import Base

class HomeContent(Base):
    __tablename__ = "home_content"

    id = Column(Integer, primary_key=True, index=True)
    ngo_name = Column(String, default="My NGO")
    about_text = Column(Text)
    mission = Column(Text)
    vision = Column(Text)
    donation_link = Column(String)
    contact_email = Column(String)
    contact_phone = Column(String)
