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
        raise NotImplementedError(f"{self} has no display name")


class JsonModel:
    def update(self, **kwargs):
        for arg, value in kwargs.items():
            if hasattr(self, arg):
                setattr(self, arg, value)
            else:
                logger.debug(f"{self} has no attribute: {arg}")

    @property
    def json(self):
        meta = {
            "display_name": self.display_name,
        }
        data = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        return {
            "meta": meta,
            "data": data,
        }


class Demo(db.Model, DisplayName, JsonModel):
    # Table settings
    __tablename__ = "demo"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        if "id" in kwargs.keys():
            self.id = kwargs.pop("id", None)
        self.name = kwargs.pop("name", None)

    def __repr__(self) -> str:
        return f"<Demo {self.name} ({self.id})>"