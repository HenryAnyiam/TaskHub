#!/usr/bin/python3
from models import storage

all = storage.all('User')
for i in all:
    print(all[i].email, all[i].notifications)

