#!/usr/bin/python3
"""module to handle message objects"""

from models.base_model import BaseModel, Base
from models.users import User
from models.tasks import Task
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class Message(BaseModel, Base):
    """class handle a new message object"""

    __tablename__ = "messages"
    text = Column(String(100), nullable=False)
    sender = Column(String(50), ForeignKey("users.id"), nullable=False)
    receiver = Column(String(50), ForeignKey("tasks.id"), nullable=False)

    if getenv("THB_STORAGE_TYPE") == "db":
        user = relationship("User", back_populates="messages")
        task = relationship("Task", back_populates="tasks")


    def __init__(self, *args, **kwargs):
        """message class initialization"""
        super().__init__(*args, **kwargs)

if getenv("THB_STORAGE_TYPE") == "db":
    User.messages = relationship("Message", order_by=Message.id, back_populates="user")
    Task.messages = relationship("Message", order_by=Message.id, back_populates="task")