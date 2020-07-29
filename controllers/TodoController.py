from flask import Flask, request, jsonify, make_response, current_app, Blueprint
from flask_sqlalchemy import SQLAlchemy
import datetime
import jwt
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from functools import  wraps
from models.models import db, Todo

tareas = Blueprint('tareas', __name__)


#  decorador para comprobar el token
def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None
		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']

		if not token:
			return jsonify({'response': 'token is missing!'}), 401

		try:
			data = jwt.decode(token, current_app.config['SECRET_KEY'])
			current_user = User.query.filter_by(public_id=data['public_id']).first()
		except:
			return jsonify({'response':'token is invalid'}), 401

		return f(current_user, *args, **kwargs)

	return decorated

@tareas.route('/tareas')
def indextodo():
	return jsonify({'msg': 'welcome to api tareas'})

@tareas.route('/todo', methods=['GET'])
@token_required
def get_all_todos(current_user):
	todos = Todo.query.filter_by(user_id=current_user.id)

	output = []

	for todo in todos:
		todo_data = {}
		todo_data['id'] = todo.id
		todo_data['text'] = todo.text
		todo_data['complete'] = todo.complete
		output.append(todo_data)


	return jsonify({"Todos":output})

@tareas.route('/todo/<todo_id>', methods=['GET'])
@token_required
def get_one_todo(current_user, todo_id):
	todo = Todo.query.filter_by(id=todo_id).first()

	if not todo:
		return jsonify({"msg": "Invalid id"})
	else:
		todo_data = {}
		todo_data['id'] = todo.id
		todo_data['text'] = todo.text
		todo_data['complete'] = todo.complete

	return jsonify({"Todos":todo_data})

@tareas.route('/todo', methods=['POST'])
@token_required
def create_todo(current_user):
	data = request.get_json()

	new_todo = Todo(text=data['text'], complete=False, user_id=current_user.id)
	db.session.add(new_todo)
	db.session.commit()

	return jsonify({'message': 'Todo created'})

@tareas.route('/todo/<todo_id>', methods=['PUT'])
@token_required
def complete_todo(current_user, todo_id):
	todo = Todo.query.filter_by(id=todo_id).first()

	if not todo:
		return jsonify({"msg": "Invalid id"})
	else:
		todo.complete = True
		db.session.commit()

	return jsonify({"Todos": todo.text+" has been completed"})


@tareas.route('/todo/<todo_id>', methods=['DELETE'])
@token_required
def delete_todo(current_user, todo_id):
	todo = Todo.query.filter_by(id=todo_id).first()

	if not todo:
		return jsonify({"msg": "Invalid id"})
	else:
		db.session.delete(todo)
		db.session.committareas

	return jsonify({"Todos": todo.text+" has been deleted"})