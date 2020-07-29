from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import FLOAT, TEXT
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class User(db.Model):
	"""Usuarios de la aplicacion"""
	__tablename__ = 'user'

	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.String(50), unique=True)
	name = db.Column(db.String(50))
	password = db.Column(db.String(80))
	admin = db.Column(db.Boolean, default=False)
	todos = relationship("Todo")

class Todo(db.Model):
	"""Tareas de un usuario, un usuario tiene una o muchas"""
	__tablename__ = 'todo'

	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(50))
	complete = db.Column(db.Boolean, default=False)
	user_id = db.Column(db.Integer, ForeignKey('user.id'))

class Product(db.Model):
	"""Cada producto, sus especificaciones y existencia en stock"""

	__tablename__ = 'product'

	id = db.Column(db.Integer, primary_key=True)
	product_name = db.Column(db.String(50), nullable=False)
	ref = db.Column(db.String(100))
	buy = db.Column(db.Integer, default=0)
	stock = db.Column(db.Integer, default=0)
	buy_price = db.Column(FLOAT)
	sell_price = db.Column(FLOAT)
	tipo = db.Column(db.Integer, ForeignKey('product_type.id'))


class ProductType(db.Model):
	__tablename__ = 'product_type'

	id = db.Column(db.Integer, primary_key=True)
	type_name = db.Column(db.String(60), nullable=False)
	desc = db.Column(TEXT)
	products = relationship("Product")
