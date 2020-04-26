from datetime import datetime
from enum import Enum

from flask.json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy
import pytz
from sqlalchemy.orm.query import Query


db = SQLAlchemy()


## Helpers

class JsonBase:
    def to_json(self, ignore_keys=None):
        ignore_keys = ignore_keys or set()

        obj = dict(self.__dict__)
        for k in list(obj.keys()):
            if k in ignore_keys or k.startswith("_"):
                del obj[k]

        return obj


class CustomJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, JsonBase):
            return obj.to_json()
        elif isinstance(obj, Query):
            return obj.all()
        elif isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, datetime):
            return obj.replace(tzinfo=pytz.UTC).isoformat()

        return super().default(obj)


## Data


class SensorType(Enum):
    AIR_TEMP = "AIR_TEMP"
    AIR_HUMIDITY = "AIR_HUMIDITY"
    SOIL_MOISTURE = "SOIL_MOISTURE"


class SensorReading(db.Model, JsonBase):
    type = db.Column(db.Enum(SensorType), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, primary_key=True)
    value = db.Column(db.Float, nullable=False)
