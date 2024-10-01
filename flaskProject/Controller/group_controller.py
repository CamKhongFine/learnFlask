from flask import jsonify, request, make_response, Blueprint
from Model.group import Group
from Model.db import db
from Model.user import User

group_controller = Blueprint('group_controller', __name__)

@group_controller.route('/groups', methods=['GET'])
def get_groups():
    try:
        groups = Group.query.all()
        groups_serialized = [group.serialize() for group in groups]
        return make_response(jsonify({'groups': groups_serialized}), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@group_controller.route('/groups', methods=['POST'])
def create_group():
    try:
        data = request.get_json()
        new_group = Group(group_name=data['group_name'])
        list_users_id = data['users']
        for id in list_users_id:
            user = User.query.get(id)
            if user:
                new_group.users.append(user)
            else:
                make_response(jsonify({'message': 'Project not found'}), 404)
        db.session.add(new_group)
        db.session.commit()
        return make_response(jsonify({'message':'Group created'}), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@group_controller.route('/groups/<int:group_id>', methods=['PUT'])
def update_group(group_id):
    try:
        group = Group.query.filter_by(group_id=group_id).first()
        if group:
            data = request.get_json()
            group.group_name = data['group_name']
            users_id = data['users']
            users_to_add = User.query.filter(User.user_id.in_(users_id)).all()
            for user in users_to_add:
                if user not in group.users:
                       group.users.append(user)
            db.session.commit()
            return make_response(jsonify({'message':'Group updated'}))
        return make_response(jsonify({'error':'Group not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@group_controller.route('/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    try:
        group = Group.query.filter_by(group_id=group_id).first()
        if group:
            db.session.delete(group)
            db.session.commit()
            return make_response(jsonify({'message':'Group deleted'}))
        return make_response(jsonify({'error':'Group not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@group_controller.route('/groups/<int:group_id>', methods=['GET'])
def get_group_by_id(group_id):
    try:
        group = Group.query.filter_by(group_id=group_id).first()
        if group:
            serialized_group = group.serialize()
            return make_response(jsonify(serialized_group), 200)
        return make_response(jsonify({'error':'Group not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)


