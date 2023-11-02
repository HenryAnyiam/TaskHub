#!/usr/bin/python3
"""module to handle message objects"""

from models.base_model import BaseModel, Base
from models.users import User
from models.teams import Team
from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from os import getenv


class Message(BaseModel, Base):
    """class handle a new message object"""

    __tablename__ = "messages"
    text = Column(String(100), nullable=False)
    sender = Column(String(50), ForeignKey("users.id"), nullable=False)
    receiver = Column(String(50), ForeignKey("teams.id"), nullable=False)
    read = Column(String(50), nullable=False)

    if getenv("THB_STORAGE_TYPE") == "db":
        user = relationship("User", back_populates="messages")
        team = relationship("Team", back_populates="messages")


    def __init__(self, *args, **kwargs):
        """message class initialization"""
        super().__init__(*args, **kwargs)
        if kwargs.get("read", None) is None:
            self.read = False

if getenv("THB_STORAGE_TYPE") == "db":
    User.messages = relationship("Message", order_by=Message.id, back_populates="user")
    Team.messages = relationship("Message", order_by=Message.id, back_populates="team")