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

def add_child(parent_id, child_id):
    """add a child task to a parent class"""
    tasks = storage.all('Task')
    parent = None
    for i in tasks:
        if parent_id in i:
            parent = tasks[i]
            break
    if parent is not None:
        parent['child_task'].append(child_id)
        storage.save()

def update_progress(id):
    """update a task progress and its parents"""
    tasks = storage.all('Task')
    task = None
    for i in tasks:
        if id in i:
            task = tasks[i]
            break
    if task is not None:
        children = len(task['child_task'])
        if children == 0:
            task['progress'] = 100
        else:
            progress = (1 / children) * 100
            task['progress'] += round(progress)
        storage.save()
        parent = task['parent']
        if parent != "None":
            update_progress(parent)

def task_messages(id):
    """gets all messages for a task"""
    all_messages = storage.all('Message')
    messages = []
    for i in all_messages:
        if i['receiver'] == id:
            messages.append(i)
    messages.sort(key=(lambda i: i['updated_at']))
    return messages

def user_notifications(id):
    """gets all notifications for a user"""
    all_notifications = storage.all('Notification')
    notifications = []
    for i in all_notifications:
        if i['user_id'] == id:
            notifications.append(i)
    notifications.sort(key=(lambda i: i['updated_at']))
    return notifications
