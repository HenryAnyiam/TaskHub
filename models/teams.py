#!/usr/bin/python3
"""module to handle team projects"""


from models.base_model import BaseModel, Base
from models.users import User
from sqlalchemy import Column, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class Team(BaseModel, Base):
    """class to handle team objects"""

    __tablename__ = "teams"
    name = Column(String(50), nullable=False)
    members = Column(JSON, nullable=False)
    messages = Column(JSON, nullable=False)
    tasks = Column(JSON, nullable=False)
    created_by = Column(String(50), ForeignKey("users.id"), nullable=False)

    if getenv("THB_STORAGE_TYPE") == "db":
        user = relationship("User", back_populates="teams")

    def __init__(self, *args, **kwargs):
        """team class initialization"""
        super().__init__(*args, **kwargs)
        if kwargs.get("messages", None) is None:
            self.messages = []
        if kwargs.get("members", None) is None:
            self.members = []
        if kwargs.get("tasks", None) is None:
            self.tasks = []


if getenv("THB_STORAGE_TYPE") == "db":
    User.teams = relationship("Team", order_by=Team.id, back_populates="user")