#!/usr/bin/python3
"""module to handle database storage"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.messages import Message
from models.users import User
from models.notifications import Notification
from models.tasks import Task
from models.teams import Team


class DBStorage:
    """use sqlalchemy to manage database"""

    __engine = None
    __session = None

    def __init__(self):
        """initialization of DBStorage"""
        db_name = getenv('THB_MYSQL_DB')
        user = getenv('THB_MYSQL_USER')
        pwd = getenv('THB_MYSQL_PWD')
        host = getenv('THB_MYSQL_HOST')
        env = getenv('THB_ENV')

        self.__engine = create_engine(f'mysql+pymysql://{user}:{pwd}@{host}/{db_name}',
                                      pool_pre_ping=True)
        
        if env == 'Test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """return all object stored"""
        classes = {'Message' : Message, 'User': User,
                   'Notifications': Notification, 'Task': Task,
                   'Team': Team}
        objects = {}
        obj = []
        obj_name = []
        length = 0
        if cls and (cls in classes):
            obj = [classes[cls]]
            obj_name = [cls]
            length = 1
        else:
            for i in classes:
                obj.append(classes[i])
                obj_name.append(i)
                length += 1
        for i in range(length):
            saved = self.__session.query(obj[i])
            for j in saved:
                key = f'{obj_name[i]}.{j.id}'
                objects[key] = j
        return objects
    
    def new(self, obj):
        """add object to current database session"""
        self.__session.add(obj)

    def save(self):
        """save current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete object from current session"""
        if obj:
            self.__session.delete(obj)
            self.save()
    
    def reload(self):
        """create table and session"""
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        scope = scoped_session(session)
        self.__session = scope()

    def clear(self):
        """drop all tables"""
        Base.metadata.drop_all(self.__engine)
