#!/usr/bin/python3
from models import storage

all = storage.all('Team')
for i in all:
    print(all[i])