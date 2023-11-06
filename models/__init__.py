#!/usr/bin/python3
"""models initialization"""

from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from os import getenv

if getenv('THB_STORAGE_TYPE') == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()
storage.reload()