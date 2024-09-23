#!/usr/bin/python3
"""DocumentStorage class Module
"""
from os import getenv
from pymongo import MongoClient

classes = {}


class DocumentStorage:
    """Interacts with the MongoDB database."""

    _client = None
    __db = None

    @property
    def _db(self):
        if self.__db is None:
            self.__db = self._client[getenv("QQ_DB", "quizquickie")]
        return self.__db

    def __init__(self):
        self._client = MongoClient()

    def new(self, obj):
        """Add the object to the current database."""
        print(obj)
        self._db[obj.__tablename__].insert_one(obj.json())

    def update(self, obj):
        """Update the object in the database."""
        self._db[obj.__tablename__].update_one({"_id": obj.id}, {"$set": obj.json()})

    def delete(self, obj):
        """Delete the object from the current database."""
        if obj is not None:
            self._db[obj.__tablename__].delete_one({"_id": obj.id})

    def save(self):
        """Placeholder for save (MongoDB auto-commits)."""
        pass

    def reload(self):
        """Reloads data from the database."""
        pass

    def close(self):
        """Close the MongoDB client connection."""
        self._client.close()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found.
        """
        if cls.__tablename__ not in classes.values():
            return None
        result = self._db[cls.__tablename__].find_one({"_id": id})
        return result

    def search(self, cls, **kwargs):
        """Search for a matching class instance."""
        return list(self._db[cls.__tablename__].find(kwargs))

    def count(self, cls=None):
        """Count the number of objects in storage."""
        count = 0
        if cls is None:
            count = sum(
                self._db[clas.__tablename__].estimated_document_count()
                for clas in classes.values()
            )
        elif cls in classes.values():
            count = self._db[cls.__tablename__].estimated_document_count()
        return count

    def all(self, cls=None):
        """Query all objects in the current database."""
        new_dict = {}
        if cls is None:
            for clas in classes.values():
                objs = self._db[clas.__tablename__].find({})
                for obj in objs:
                    key = clas.__name__ + "." + str(obj["_id"])
                    new_dict[key] = obj
        else:
            objs = self._db[cls.__tablename__].find({})
            for obj in objs:
                key = cls.__name__ + "." + str(obj["_id"])
                new_dict[key] = obj
        return new_dict


# Example usage
if __name__ == "__main__":
    db = DocumentStorage()
    db.reload()

    class T:
        __tablename__ = "t"
        id = 69
        h = "hello"
        w = "world"

        def json(self):
            return self.__dict__

    db.new(T())  # Add the object to the database
    db.new(T())
    db.new(T())

    # Retrieve object by id
    obj = db.all(T)
    print(obj)

    # Check if count is correct
    if not db.count(T) == 3:
        print(db.count(T))
        assert False
