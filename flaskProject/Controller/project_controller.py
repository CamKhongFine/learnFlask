from flask import jsonify, request, make_response, Blueprint
import json

from Model.db import db
from Model.project import Project

project_controller = Blueprint('project_controller', __name__)

@project_controller.route('/projects', methods=['GET'])
def get_projects():
    try:
        projects = Project.query.all()
        project_serialized = [project.serialize() for project in projects]
        return make_response(jsonify({'projects': project_serialized}), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@project_controller.route('/projects', methods=['POST'])
def create_project():
    try:
        data = request.get_json()
        new_project = Project(project_name=data['project_name'], description=data['description'])
        db.session.add(new_project)
        db.session.commit()
        return make_response(jsonify({'message':'Project created'}), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@project_controller.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    try:
        project = Project.query.filter_by(project_id=project_id).first()
        if project:
            data = request.get_json()
            project.project_name = data['project_name']
            project.description = data['description']
            db.session.commit()
            return make_response(jsonify({'message':'Project updated'}))
        return make_response(jsonify({'error':'Project not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@project_controller.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    try:
        project = Project.query.filter_by(project_id=project_id).first()
        if project:
            db.session.delete(project)
            db.session.commit()
            return make_response(jsonify({'message':'Project deleted'}))
        return make_response(jsonify({'error':'Project not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@project_controller.route('/projects/<int:project_id>', methods=['GET'])
def get_project_by_id(project_id):
    try:
        project = Project.query.filter_by(project_id=project_id).first()
        if project:
            serialized_project = project.serialize()
            return make_response(jsonify(serialized_project, 200))
        return make_response(jsonify({'error':'Project not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)


