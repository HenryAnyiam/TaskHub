#!/usr/bin/python3
"""module to handle Notification objects"""

from models.base_model import BaseModel


class Notification(BaseModel):
    """class handle a new Notification object"""

    def __init__(self, *args, **kwargs):
        """Notification class initialization"""
        super().__init__(*args, **kwargs)