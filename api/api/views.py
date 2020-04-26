from datetime import datetime
import os

from flask import Blueprint, current_app, jsonify, render_template

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


# Serve React App


@bp.route('/')
def serve():
    return render_template('index.html')
