from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
baseDir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(baseDir, "db.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

# Product schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "price", "qty")

# Init schema
productSchema = ProductSchema(strict=True)
productsSchema = ProductSchema(many=True, strict=True)

# Create a product
@app.route("/product", methods=["POST"])
def addProduct():
    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    qty = request.json["qty"]

    createdProduct = Product(name, description, price, qty)

    db.session.add(createdProduct)
    db.session.commit()

    return productSchema.jsonify(createdProduct)

# Get all products
@app.route("/product", methods=["GET"])
def getAllProducts():
    allProducts = Product.query.all()
    result = productsSchema.dump(allProducts)

    return jsonify(result.data)

# Get a single product
@app.route("/product/<id>", methods=["GET"])
def getSingleProduct(id):
    singleProduct = Product.query.get(id)
    return productSchema.jsonify(singleProduct)

# Update a product
@app.route("/product/<id>", methods=["PUT"])
def updateProduct(id):
    product = Product.query.get(id)

    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    qty = request.json["qty"]

    product.name = name
    product.description = description
    product.price = price
    product.qty = qty

    db.session.commit()

    return productSchema.jsonify(product)

# Remove a product
@app.route("/product/<id>", methods=["DELETE"])
def removeProduct(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return productSchema.jsonify(product)

# Run server
if __name__ == "__main__":
    app.run(debug=True)
