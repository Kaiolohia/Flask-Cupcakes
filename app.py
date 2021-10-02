"""Flask app for Cupcakes"""
from flask import Flask, json, render_template, redirect, request, flash, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = 'nimdA'

connect_db(app)
db.create_all()

"""API ROUTES"""


@app.route('/api/cupcakes', methods = ["GET"])
def send_all_cupcakes():
    res = Cupcake.query.all()
    serialized = [Cupcake.serialize(item) for item in res]
    return jsonify(cupcakes = serialized)

@app.route('/api/cupcakes/<int:id>', methods = ["GET"])
def send_cupcake(id):
    res = Cupcake.query.filter_by(id = id).first_or_404()
    return jsonify(cupcake = Cupcake.serialize(res))

@app.route('/api/cupcakes', methods = ["POST"])
def add_new_cupcake():
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]
    new_cupcake = Cupcake(flavor = flavor, size = size, rating = rating, image = image)
    db.session.add(new_cupcake)
    db.session.commit()
    return (jsonify(cupcake = Cupcake.serialize(new_cupcake)), 201)

@app.route('/api/cupcakes/<int:id>', methods = ["PATCH"])
def update_cupcake(id):
    cur_cupcake = Cupcake.query.filter_by(id = id).first_or_404()
    cur_cupcake.flavor = request.json.get("flavor", cur_cupcake.flavor)
    cur_cupcake.size = request.json.get("size", cur_cupcake.size)
    cur_cupcake.rating = request.json.get("rating", cur_cupcake.rating)
    cur_cupcake.image = request.json.get("image", cur_cupcake.image)
    db.session.commit()
    return jsonify(cupcake = Cupcake.serialize(cur_cupcake))

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    cur_cupcake = Cupcake.query.filter_by(id = id).first_or_404()
    db.session.delete(cur_cupcake)
    db.session.commit()
    return jsonify(message = "Deleted")

"""VISUAL ROUTES"""

@app.route('/')
def show_home_page():
    return render_template('home.html')