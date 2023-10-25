#!/usr/bin/python3
"""module to handle Notification objects"""

from models.base_model import BaseModel, Base
from models.users import User
from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from os import getenv


class Notification(BaseModel, Base):
    """class handle a new Notification object"""

    __tablename__ = "notifications"
    title = Column(String(50), nullable=False)
    type = Column(String(50), nullable=False)
    check = Column(Boolean, nullable=False)
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False)

    if getenv("THB_STORAGE_TYPE") == "db":
        user = relationship("User", back_populates="notifications")

    def __init__(self, *args, **kwargs):
        """Notification class initialization"""
        super().__init__(*args, **kwargs)

if getenv("THB_STORAGE_TYPE") == "db":
    User.notifications = relationship("Notification", order_by=Notification.id, back_populates="user")