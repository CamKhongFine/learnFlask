from Model.db import db

class Project(db.Model):
    __tablename__ = 'projects'

    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(120), nullable=False)

    def serialize(self):
        return {
            'project_id': self.project_id,
            'project_name': self.project_name,
            'description': self.description,
            'users': [user.serialize_for_project() for user in self.users]
        }

    def serialize_for_user(self):
        return {
            'project_id': self.project_id,
            'project_name': self.project_name,
            'description': self.description
        }