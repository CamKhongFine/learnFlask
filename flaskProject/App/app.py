from flask import Flask

from Controller.user_controller import user_controller
from Controller.group_controller import group_controller
from Controller.project_controller import project_controller
from Model.db import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('Config.config')

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(user_controller)
    app.register_blueprint(group_controller)
    app.register_blueprint(project_controller)

    return app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)