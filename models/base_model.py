#!/usr/bin/python3
"""
Contains class BaseModel
"""
from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

time = "%Y-%m-%dT%H:%M:%S.%f"

if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Instantiate a new model."""
        self.id = str(uuid.uuid4())
        self.created_at = self.updated_at = datetime.now()

        # Set each keyword argument as an instance attribute
        for k, v in kwargs.items():
            # Do not set `__class__`, since it is set automatically
            if k == '__class__':
                continue

            # Convert datetime strings to datetime objects
            if k in ('updated_at', 'created_at'):
                v = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%f')

            setattr(self, k, v)

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """
        Updates the attribute 'updated_at' with the current datetime and saves
        self in the storage engine
        """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
        models.storage.save()
