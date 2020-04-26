#!/usr/bin/env python

import os

from api import create_app


app = create_app()

if not os.path.exists("app.db"):
    from api.models import db

    with app.app_context():
        db.create_all()

app.run(debug=app.config['DEBUG'])
