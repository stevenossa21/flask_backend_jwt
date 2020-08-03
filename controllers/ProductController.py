from flask import Flask, request, jsonify, make_response, current_app, Blueprint
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import text
import datetime
import jwt
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from functools import  wraps
from models.models import db, Product, ma
import simplejson as json


products = Blueprint('products', __name__)


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


"""schemas de marshmallow"""
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ('id', 'product_name', 'ref', 'buy', 'stock', 'buy_price', 'sell_price', 'tipo')

class TipoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ('product_name','type_name')

class StadsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ('compra','stock', 'gastado', 'vendido')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
tipos_schema = TipoSchema(many=True)
stads_schema = StadsSchema()



@products.route('/productos')
def indextodo():
	return jsonify({'msg': 'welcome to api products'})

@products.route('/products', methods=['GET'])
def get_all_products():
	products = Product.query.all()
	result = products_schema.dump(products)
	return jsonify(result)

@products.route('/tipo', methods=['GET'])
def tipo():
	sql = text("""SELECT product.product_name, product_type.type_name FROM product INNER JOIN product_type ON product.tipo=product_type.id""") 
	result = db.engine.execute(sql)
	print('result: ', result)
	result = tipos_schema.dump(result)
	return jsonify(result)

@products.route('/product/stads', methods=['GET'])
def stads():
	sql = text("""SELECT SUM(buy) as 'compra', SUM(stock) as 'stock', SUM(buy_price) as 'gastado', SUM(sell_price) as 'vendido' FROM product""")
	result = db.engine.execute(sql).first()
	result = stads_schema.dump(result)
	totalBuy = int(result['compra'])
	totalStock = int(result['stock'])
	totalGasto = float(result['gastado'])
	totalVenta = float(result['vendido'])
	response = {'comprado': totalBuy, 'vendido': totalBuy-totalStock, 'stock': totalStock, 'ganancia': totalVenta-totalGasto, 'precio_compra': totalGasto, 'precio_venta': totalVenta}
	return jsonify(response)
