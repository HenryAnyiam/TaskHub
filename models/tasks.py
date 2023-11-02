#!/usr/bin/python3
"""module to handle task objects"""

from models.base_model import BaseModel, Base
from models.users import User
from sqlalchemy import Column, String, DateTime, Integer, JSON, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class Task(BaseModel, Base):
    """class handle a new task object"""

    __tablename__ = "tasks"
    title = Column(String(100), nullable=False)
    parent = Column(String(50), nullable=False)
    team = Column(String(50), nullable=True)
    child_task = Column(JSON, nullable=False)
    progress = Column(Integer, nullable=False)
    created_by = Column(String(50), ForeignKey("users.id"), nullable=False)
    deadline = Column(DateTime, nullable=True)

    if getenv("THB_STORAGE_TYPE") == "db":
        user = relationship("User", back_populates="tasks")

    def __init__(self, *args, **kwargs):
        """task class initialization"""
        super().__init__(*args, **kwargs)
        if kwargs.get('child_task', None) is None:
            self.child_task = []
        if kwargs.get('progress', None) is None:
            self.progress = 0
        if kwargs.get("parent", None) is None:
            self.parent = "None"


if getenv("THB_STORAGE_TYPE") == "db":
    User.tasks = relationship("Task", order_by=Task.id, back_populates="user")