import datetime

from db.base import Base
from sqlalchemy import BigInteger, Column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy_utils import ChoiceType


class User(Base):
    __tablename__ = "users"

    STATUSES = [
        ("finished", "finished"),
        ("dead", "dead"),
        ("alive", "alive"),
    ]

    id = Column(BigInteger, primary_key=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.current_timestamp()
    )
    status = Column(ChoiceType(STATUSES), default="alive")
    status_updated_at = Column(
        TIMESTAMP(timezone=True), onupdate=datetime.datetime.now()
    )
