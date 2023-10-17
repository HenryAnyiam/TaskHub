#!/usr/bin/python3
"""module to handle user objects"""

from hashlib import md5
from models.base_model import BaseModel


class User(BaseModel):
    """class handle a new user object"""

    def __init__(self, *args, **kwargs):
        """user class initialization"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """reset the password arg with an md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)