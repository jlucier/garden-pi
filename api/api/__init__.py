from flask import Flask

from . import views, models, scheduler

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    models.db.init_app(app)

    # TODO scheduler.scheduler.configure(**)
    scheduler.scheduler.init_app(app)
    scheduler.scheduler.start()

    app.register_blueprint(views.bp)
    app.json_encoder = models.CustomJsonEncoder

    return app
