from datetime import datetime

from flask import Blueprint, current_app, jsonify

from .models import *


bp = Blueprint('/', __name__)

@bp.route('/current')
def get_current_readings():
    return jsonify({
        "data": SensorReading.query.order_by(SensorReading.timestamp.desc()).distinct(SensorReading.type).limit(2),
    })

@bp.route('/all')
def all_readings():
    return jsonify({
        "data": SensorReading.query.order_by(SensorReading.timestamp.asc())
    })
