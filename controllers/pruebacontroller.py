from flask import Flask, jsonify, Blueprint

prueba = Blueprint('prueba', __name__)

@prueba.route('/prueba')
def pruebaIndex():
	return jsonify({'msg':'probando'})