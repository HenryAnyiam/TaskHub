#!/usr/bin/python3
"""module to handle user objects"""

from hashlib import md5
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, JSON
from flask_login import UserMixin


class User(BaseModel, UserMixin, Base):
    """class handle a new user object"""

    __tablename__ = "users"
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    notifications = Column(JSON, nullable=False)

    def __init__(self, *args, **kwargs):
        """user class initialization"""
        super().__init__(*args, **kwargs)
        if kwargs.get("notifications", None) is None:
            self.notifications = []

    def __setattr__(self, name, value):
        """reset the password arg with an md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)

    def get_id(self):
        return self.id