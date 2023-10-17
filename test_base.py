#!/usr/bin/python3
from models.tasks import Task
from models.base_model import BaseModel
from models import storage, add_child, update_progress

all_obj = storage.all()
task1 = all_obj["Task.69865124-b389-4005-87f0-512cca3275ec"]
print(task1)