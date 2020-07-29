
from flask import Flask , jsonify
from config import DevelopmentConfig
from config import  PORT
from flask_sqlalchemy import SQLAlchemy
from models.models import db
from controllers.pruebacontroller import prueba
from controllers.UserController import usuarios
from controllers.TodoController import tareas

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

@app.route('/')
def index():
	return jsonify({'response':'welcome to flask api'}) 

app.register_blueprint(prueba)
app.register_blueprint(usuarios)
app.register_blueprint(tareas)

if __name__== '__main__':
	with app.app_context():
		db.create_all() #crea todas las tablas que no esten creadas en la BD
	app.run(debug=True, port=int(PORT))
