#!/usr/bin/python3
"""RelationalStorage class Module
"""
from os import getenv
from collections.abc import Callable
from typing import Any
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Query


class RelationalStorage:
    """interacts with the SQL database"""

    _engine = None
    _session = None

    def __init__(self):
        """initialise the storage engine instance"""
        if getenv("QQ_DB_ENGINE", "SQLITE") == "MYSQL":
            DB_NAME = getenv("QQ_DB_NAME", "quizquickie_db")
            DB_USR = getenv("QQ_DB_USR", "quizquickie_usr")
            DB_PWD = getenv("QQ_DB_PWD", "quizquickie_pwd")
            DB_HOST = getenv("QQ_DB_HOST", "localhost")

            self._engine = create_engine(
                f"mysql+mysqldb://{DB_USR}:{DB_PWD}@{DB_HOST}/{DB_NAME}"
            )
        else:
            DB = getenv("QQ_DB", "quizquickie_db")
            self._engine = create_engine(f"sqlite:///{DB}.db")

    def new(self, obj):
        """add the object to the current database session"""
        if obj is not None:
            self._session.add(obj)
        return obj

    def update(self, obj):
        if obj is not None:
            self._session.merge(obj)
        return obj

    def delete(self, obj):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self._session.delete(obj)
        return obj

    def save(self):
        """commit all changes of the current database session"""
        self._session.commit()

    def cleanup(self):
        """rollback the changes that happened in the transaction"""
        self._session.rollback()

    def reload(self):
        """reloads data from the database"""
        from models.base import Base

        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        session_factory = sessionmaker(bind=self._engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self._session = Session()

    def close(self):
        """remove the session from the running storage engine"""
        self._session.close()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        from models import classes

        if cls not in classes.values():
            return None

        return self._session.query(classes[cls]).get(id)

    def search(self, cls, **kwargs):
        """Search for a matching class instance"""
        return self._session.query(cls).filter_by(**kwargs).all()

    def count(self, cls=None):
        """count the number of objects in storage"""
        from models import classes

        count = 0

        if not cls:
            count = sum(self._session.query(clas).count() for clas in classes.values())
        elif cls in classes.values():
            count = self._session.query(cls).count()
        return count

    def all(self, cls=None):
        """query on the current database session"""
        from models import classes

        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self._session.query(classes[clss]).all()
                for obj in objs:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    new_dict[key] = obj
        return new_dict

    def query(self, *args, **kwargs):
        return self._session.query(*args, **kwargs)


if __name__ == "__main__":
    db = RelationalStorage()

    from models import classes
    from models.base import Base
    from sqlalchemy import Column, Integer, String

    class T(Base):
        __tablename__ = "t"
        id = Column(Integer, primary_key=True)
        h = Column(String, default="hello")
        w = Column(String, default="world")

        def __repr__(self):
            return repr(self.json())

        def json(self):
            return self.__dict__

    classes["t"] = T
    db.reload()

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


def paginate(
    item_name: str,
    query: Query,
    page: int = None,
    page_size: int = None,
    apply: Callable[[Any], dict] = None,
):
    """Helper function to paginate SQLAlchemy queries"""
    if page is None:
        page = 1
    if page_size is None:
        page_size = getenv("PAGE_SIZE")
    page = int(page)
    page_size = int(page_size)
    if page < 1:
        raise ValueError("page")
    if page_size < 1:
        raise ValueError("page_size")

    total_items = query.count()
    total_pages = (
        total_items + page_size - 1
    ) // page_size  # Round up to get total pages
    items = query.limit(page_size).offset((page - 1) * page_size).all()

    return {
        item_name: [apply(item) if apply else item.to_dict() for item in items],
        "page": page,
        "next": page + 1 if page < total_pages else page,
        "prev": page - 1 if page > 1 else page,
        "page_size": page_size,
        f"total_{item_name}": total_items,
        "total_pages": total_pages,
    }
