#!/usr/bin/python3
"""module to handle file storage"""

import json

class FileStorage:
    """class to handle storing and reloading storage file"""

    __file_path = 'file.json' #file to store serialized objects
    __objects = {} #dictionary to store deserialized objects
    __classes = ["Task", "Notification",
                 "Message", "User"]

    def all(self, cls=None) -> dict:
        """returns all objects stored"""
        if cls:
            new_dict = {}
            if cls in self.__classes:
                for i in self.__objects:
                    if cls in i:
                        new_dict[i] = self.__objects[i]
            return new_dict
        return self.__objects
    
    def new(self, obj):
        """adds a new object to __objects"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj.to_dict()

    def save(self):
        """saved serialized self.__objects to __file_path"""
        with open(self.__file_path, 'w', encoding="UTF-8") as my_file:
            json.dump(self.__objects, my_file)
    
    def reload(self):
        """reloads objects from file storage"""
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as my_file:
                self.__objects = json.load(my_file)
        except Exception:
            pass