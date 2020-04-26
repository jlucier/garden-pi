from datetime import datetime

from flask import Blueprint, current_app, jsonify

from .models import *


bp = Blueprint('/', __name__)

@bp.route('/current')
def get_current_readings():
    return jsonify({
        "data": [
            SensorReading.query.order_by(SensorReading.timestamp.desc()).filter_by(type=SensorType.AIR_TEMP).first(),
            SensorReading.query.order_by(SensorReading.timestamp.desc()).filter_by(type=SensorType.AIR_HUMIDITY).first(),
        ],
    })

@bp.route('/all')
def all_readings():
    return jsonify({
        "data": SensorReading.query.order_by(SensorReading.timestamp.asc())
    })
