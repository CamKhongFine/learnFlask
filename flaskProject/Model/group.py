
from Model.db import db

class Group(db.Model):
    __tablename__ = 'groups'

    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50), nullable=False, unique=True)
    users = db.relationship('User', backref='group', lazy='subquery')

    def serialize(self):
        return {
            "group_id" : self.group_id,
            "group_name" : self.group_name,
            "users": [user.serialize_for_project() for user in self.users]
        }