from tasks.tasks import flask_app
from controller.tasks_controller import task


flask_app.register_blueprint(task)

if __name__ == '__main__':
    flask_app.run()