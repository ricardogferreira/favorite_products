import os

from celery import Celery
from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

config_file = os.environ.get("CONFIG", "favorite_products.config")

app = Flask(__name__)
app.config.from_object(config_file)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app, prefix="/api")


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config["CELERY_BROKER_URL"]
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)
