#!/usr/bin/python3
"""module to define basemodel"""

import uuid
from datetime import datetime
from models import storage

class BaseModel:
    """base class with common attribute for other classes"""

    def __init__(self, *args, **kwargs) -> None:
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if (key == 'created_at') or (key == 'updated_at'):
                        value = datetime.fromisoformat(value)
                    setattr(self, key, value)
            if kwargs.get('id') is None:
                self.id = str(uuid.uuid4())
            if kwargs.get('created_at') is None:
                self.created_at = datetime.now()
            if kwargs.get('uodated_at') is None:
                self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self) -> str:
        """string representation of class"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
    
    def save(self):
        """save changes to object"""
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """returns a dictionary representation of the class"""
        new_dict = self.__dict__.copy()
        new_dict['__class__'] = self.__class__.__name__
        new_dict['updated_at'] = new_dict['updated_at'].isoformat()
        new_dict['created_at'] = new_dict['created_at'].isoformat()
        return new_dict