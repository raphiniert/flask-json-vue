import logging

from datetime import datetime
from sqlalchemy import func, DateTime

from flaskjsonvue.db import db

logger = logging.getLogger("flaskjsonvue")


class DisplayName:
    @property
    def display_name(self):
        if hasattr(self, "name"):
            return self.name
        raise NotImplementedError(f"{self.__class__.__name__} has no display name")


class JsonModel(DisplayName):
    def init(self, **kwargs):
        for arg, value in kwargs.items():
            if hasattr(self, arg):
                for col in self.__table__.columns:
                    if col.name == arg:
                        if isinstance(col.type, DateTime):
                            value = datetime.fromisoformat(value)
                        setattr(self, arg, value)
                        break
            else:
                logger.info(f"{self.__class__.__name__} has no attribute: '{arg}'")

    def update(self, **kwargs):
        for arg, value in kwargs.items():
            if hasattr(self, arg):
                if isinstance(getattr(self, arg), datetime):
                    value = datetime.fromisoformat(value)
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
        data = {
            col.name: self.__format_json_value(getattr(self, col.name))
            for col in self.__table__.columns
        }
        return {
            "meta": meta,
            "data": data,
        }

    def __format_json_value(self, value):
        if isinstance(value, datetime):
            return value.astimezone().isoformat()
        return value


class Demo(db.Model, JsonModel):
    # Table settings
    __tablename__ = "demo"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    decimal_value = db.Column(db.DECIMAL, nullable=False)
    entry_date = db.Column(
        db.DateTime(timezone=True), nullable=False, default=func.now()
    )

    def __init__(self, **kwargs):
        self.init(**kwargs)

    def __repr__(self) -> str:
        return f"<Demo {self.name} ({self.id})>"
