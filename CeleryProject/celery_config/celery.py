from app.app import flask_app

celery_app = flask_app.extensions["celery"]