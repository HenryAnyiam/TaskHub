#!/usr/bin/python3
"""module to handle task objects"""

from models.base_model import BaseModel
from models import storage


class Task(BaseModel):
    """class handle a new task object"""

    def __init__(self, *args, **kwargs):
        """task class initialization"""
        super().__init__(*args, **kwargs)
        if kwargs.get('child_task', None) is None:
            self.child_task = []
        if kwargs.get('progress', None) is None:
            self.progress = 0
        if kwargs.get("parent", None) is None:
            self.parent = "None"