from Model.db import db

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    projects = db.relationship('Project', secondary='users_projects', lazy='subquery',backref=db.backref('users', lazy=True))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'))

    def serialize(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'email': self.email,
            'project': [project.serialize_for_user() for project in self.projects],
            'group_id': self.group_id,
            'group_name': self.group.group_name
        }

    def serialize_for_project(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'email': self.email,
            'group_id': self.group_id,
            'group_name': self.group.group_name
        }
#The Intermediate Table
users_projects = db.Table('users_projects',
                              db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True),
                              db.Column('project_id', db.Integer, db.ForeignKey('projects.project_id'),
                                        primary_key=True))