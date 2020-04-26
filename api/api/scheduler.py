import atexit
from functools import wraps

from apscheduler.schedulers.background import BackgroundScheduler
import adafruit_dht
import board

from .models import db, SensorReading, SensorType


class FlaskScheduler(BackgroundScheduler):
    _singleton = None

    def __new__(cls):
        if cls._singleton:
            return cls._singleton

        cls._singleton = super().__new__(cls)
        return cls._singleton

    def __init__(self, app=None, shutdown_wait=True, **kwargs):
        super().__init__(**kwargs)

        atexit.register(self.shutdown, wait=shutdown_wait)
        if app:
            self.init_app(app)

        self.add_job(
            AirMonitor(), trigger="cron", second="*/5", max_instances=1, coalesce=True, misfire_grace_time=30
        )

    def init_app(self, app):
        self.app = app

    def shutdown(self, wait=True):
        if self.running:
            super().shutdown(wait=wait)


def _ctx_wrapper(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        with scheduler.app.app_context():
            return f(*args, **kwargs)

    return wrapped


class AirMonitor:
    def __init__(self, dht_pin=board.D4):
        self.dht = adafruit_dht.DHT22(dht_pin)

    @_ctx_wrapper
    def __call__(self):
        temp = self.dht.temperature
        humidity = self.dht.humidity

        db.session.add_all([
            SensorReading(value=temp, type=SensorType.AIR_TEMP),
            SensorReading(value=humidity, type=SensorType.AIR_HUMIDITY),
        ])
        db.session.commit()


scheduler = FlaskScheduler()
