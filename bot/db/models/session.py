from db.base import Base
from sqlalchemy import Column, Text, String


class Session(Base):
    __tablename__ = "api_session"

    api_name = Column(String)
    session_string = Column(Text, primary_key=True)
