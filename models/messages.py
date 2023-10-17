#!/usr/bin/python3
"""module to handle message objects"""

from models.base_model import BaseModel


class Message(BaseModel):
    """class handle a new message object"""

    def __init__(self, *args, **kwargs):
        """message class initialization"""
        super().__init__(*args, **kwargs)