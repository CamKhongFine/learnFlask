from flask import Blueprint, request, jsonify, make_response
from Model.db import db
from Model.user import User
from Model.project import Project

user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'test route'}), 200)


# create a user
@user_controller.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(user_name=data['user_name'], email=data['email'])
        project_id_list = data['project']
        for id in project_id_list:
            project = Project.query.filter_by(project_id=id).first()
            if project:
                new_user.projects.append(project)
            else:
                return make_response(jsonify({'message': 'Project not found'}), 404)
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'message': 'User created'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': str(e)}), 404)

#Get all users
@user_controller.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        users_serialized = [user.serialize() for user in users]
        return make_response(jsonify(users_serialized), 200)
    except Exception as e:
        return make_response(e, 500)

#Update a user by id
@user_controller.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.query.filter_by(user_id=id).first()
        if user:
            data = request.get_json()
            user.username = data['user_name']
            user.email = data['email']
            project_id = data['project']
            projects_to_add = Project.query.filter(Project.project_id.in_(project_id)).all()
            for project in projects_to_add:
                if project not in user.projects:
                    user.projects.append(project)
            db.session.commit()
            return make_response(jsonify({'message': 'user updated'}), 200)
        return make_response(jsonify({'message': 'error updating user'}),404)
    except Exception as e:
        return make_response(jsonify(str(e)), 500)

#delete an user by id
@user_controller.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.filter_by(user_id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'message': 'user deleted'}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error deleting user'}), 500)

@user_controller.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.filter_by(user_id=id).first();
    if user:
        serialized_user = user.serialize()
        return make_response(serialized_user, 200)
    return make_response(jsonify({'message': 'User not found'}), 404)