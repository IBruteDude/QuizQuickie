from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

time_fmt = "%Y-%m-%dT%H:%M:%S.%f"

Base = declarative_base()


class BaseModel:
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )

    def __init__(self, **kwargs):
        """initialization of the base model"""
        super().__init__(**kwargs)
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __str__(self):
        """string representation of the BaseModel class"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def update(self, **kwargs):
        """update attributes of the model"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        from models import storage

        storage.update(self)
        storage.save()
        return self

    def save(self):
        """update 'updated_at' and commit changes"""
        from models import storage

        storage.new(self)
        storage.save()
        return self

    def delete(self):
        """delete the current instance from storage"""
        from models import storage

        storage.delete(self)
        storage.save()
        return self

    def to_dict(self) -> dict:
        """return a dictionary containing all keys/values of the instance"""
        return self.to_safe_dict(self.__dict__)

    def to_safe_dict(self, obj_dict) -> dict:
        """remove private fields from the instance"""
        if "created_at" in obj_dict:
            obj_dict["created_at"] = obj_dict["created_at"].strftime(time_fmt)
        if "updated_at" in obj_dict:
            obj_dict["updated_at"] = obj_dict["updated_at"].strftime(time_fmt)
        if "_sa_instance_state" in obj_dict:
            del obj_dict["_sa_instance_state"]
        obj_dict[f"{self.__tablename__}_id"] = obj_dict["id"]
        del obj_dict["id"]
        return obj_dict
