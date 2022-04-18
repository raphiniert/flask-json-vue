import logging

from datetime import datetime
from sqlalchemy import func, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from flaskjsonvue.db import db

logger = logging.getLogger("flaskjsonvue")


class DisplayName:
    @property
    def display_name(self):
        if hasattr(self, "name"):
            return self.name
        raise NotImplementedError(f"{self.__class__.__name__} has no display name")


class JsonModel(DisplayName):
    def update(self, **kwargs):
        for arg, value in kwargs.items():
            if hasattr(self, arg):
                setattr(self, arg, value)
            else:
                logger.info(f"{self.__class__.__name__} has no attribute: '{arg}'")

    @property
    def json(self):
        if not hasattr(self, "__table__"):
            raise NotImplementedError(f"{self.__class__.__name__} has no table")
        meta = {
            "display_name": self.display_name,
        }
        data = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        return {
            "meta": meta,
            "data": data,
        }


class Demo(db.Model, JsonModel):
    # Table settings
    __tablename__ = "demo"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        self.update(**kwargs)

    def __repr__(self) -> str:
        return f"<Demo {self.name} ({self.id})>"
