""" Base module
"""

from datetime import datetime, timezone
from typing import TypeVar, List, Iterable
from os import path
import json
from random import randint
import uuid
from sqlalchemy import Column, INTEGER, DATETIME, UUID
from sqlalchemy.ext.declarative import declarative_base

time_fmt = "%Y-%m-%dT%H:%M:%S.%f"

Base = declarative_base()


class BaseModel:
    """The BaseModel class from which future classes will be derived"""

    __tablename__ = ""
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    created_at = Column(DATETIME, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DATETIME, default=lambda: datetime.now(timezone.utc))

    def __init__(self, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            for time_key in ("created_at", "updated_at"):
                if kwargs.get(time_key, False):
                    if type(kwargs[time_key]) is datetime:
                        setattr(self, time_key, kwargs[time_key])
                    else:
                        setattr(
                            self,
                            time_key,
                            datetime.strptime(kwargs[time_key], time_fmt),
                        )
                else:
                    self.updated_at = datetime.now(timezone.utc)
            if not kwargs.get("id", False):
                self.id = randint(0, 0xFFFFFFFF)
        else:
            self.id = randint(0, 0xFFFFFFFF)
            self.created_at = datetime.now(timezone.utc)
            self.updated_at = self.created_at

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:d}) {}".format(
            self.__class__.__name__, self.id, self.__dict__
        )

    def update(self, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        from models import storage

        self.updated_at = datetime.now(timezone.utc)
        storage.update(self)

    def delete(self):
        """delete the current instance from the storage"""
        from models import storage

        storage.delete(self)

    def json(self):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = self.__class__.__name__
        return self._dict_filter(new_dict)

    def _dict_filter(self, obj_dict):
        """remove private fields from instance"""
        if "created_at" in obj_dict:
            obj_dict["created_at"] = obj_dict["created_at"].strftime(time_fmt)
        if "updated_at" in obj_dict:
            obj_dict["updated_at"] = obj_dict["updated_at"].strftime(time_fmt)
        if "_sa_instance_state" in obj_dict:
            del obj_dict["_sa_instance_state"]
        return obj_dict
