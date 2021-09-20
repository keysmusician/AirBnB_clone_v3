#!/usr/bin/python3
"""Tests for .get() and .count() methods used in storage"""
from models import storage

# count
print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count("State")))

# get
first_state_id = list(storage.all("State").values())[0].id
print("First state: {}".format(storage.get("State", first_state_id)))
