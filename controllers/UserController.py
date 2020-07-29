from flask import Flask, request, jsonify, make_response, Blueprint, current_app
from flask_sqlalchemy import SQLAlchemy
import datetime
import jwt
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from functools import  wraps
from models.models import db, User

usuarios = Blueprint('usuarios', __name__)

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

@usuarios.route('/usuarios')
def indexuser():
	return jsonify({'msg': 'welcome to api usuarios'})

@usuarios.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):

	if not current_user.admin:
		return jsonify({'message': 'Cannot perform that option'})

	users = User.query.all()

	output = []

	#para esto es el marshmallow ?

	for user in users:
		user_data = {}
		user_data['public_id'] = user.public_id
		user_data['name'] = user.name
		user_data['password'] = user.password
		user_data['admin'] = user.admin
		output.append(user_data)

	return jsonify({"users": output}) 
	

@usuarios.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):
	user = User.query.filter_by(public_id=public_id).first()

	if not user:
		return jsonify({"msg": "User not found"})

	user_data = {}
	user_data['public_id'] = user.public_id
	user_data['name'] = user.name
	user_data['password'] = user.password
	user_data['admin'] = user.admin

	return jsonify({"User": user_data}) 

@usuarios.route('/user', methods=['POST']) ##register
@token_required
def create_user(current_user):
	data = request.get_json()

	hashed_password = generate_password_hash(data['password'], method='sha256')

	new_user = User(public_id=str(uuid.uuid4()),name=data['name'], password=hashed_password, admin=False)
	db.session.add(new_user)
	db.session.commit()
	return jsonify({'msg': 'new user was created successfully from flask api and jwt'})

@usuarios.route('/user/<name>', methods=['PUT'])
@token_required
def promote_user(name):
	user = User.query.filter_by(name=name).first()

	if not user:
		return jsonify({"msg": "User not found to promote"})
	else:
		user.admin = True
		db.session.commit()

	return jsonify({"msg": "The user has been promoted"})

@usuarios.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user,public_id):
	user = User.query.filter_by(public_id=public_id).first()

	if not user:
		return jsonify({"msg": "User not found to delete"})
	else:
		username = user.name
		db.session.delete(user)
		db.session.commit()

		msg = "{} was deleted successfully".format(username)

	return jsonify({"msg": msg})

@usuarios.route('/login')
def login():
	auth = request.authorization

	if not auth or not auth.username or not auth.password:
		return make_response('Could not verify password and username', 401, {'WWW-Authenticate':'Basic realm="Login required"'})
	else:
		user = User.query.filter_by(name=auth.username).first()
		if not user:
		    return make_response('Could not verify user in db', 401, {'WWW-Authenticate':'Basic realm="Login required"'})
		else:
			if check_password_hash(user.password, auth.password):
				token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, current_app.config['SECRET_KEY'])
				return jsonify({'token': token.decode('UTF-8')})
			else:
				return jsonify({'msg': 'invalid password'})

@usuarios.route('/ingresar', methods=['POST'])
def ingresar():
	data = request.get_json()
	user = User.query.filter_by(name=data['name']).first()

	if not user:
		return jsonify({"msg": "El nombre de usuario no esta asociado a ninguna cuenta"}), 401
	if check_password_hash(user.password, data['password']): #Compara el password cifrado de la bd con el password enviado en req sin cifrar
		token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, current_app.config['SECRET_KEY'])
		return jsonify({'token': token.decode('UTF-8')})
	else:
		return jsonify({'msg': 'contraseña incorrecta'}), 401