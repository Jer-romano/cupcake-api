"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from models import Cupcake, connect_db, db
from flask_debugtoolbar import DebugToolbarExtension
from forms import CupcakeForm


app = Flask(__name__)
CORS(app)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'My secret key'

connect_db(app)
db.create_all()

debug = DebugToolbarExtension(app)

@app.route("/api/cupcakes", methods=["GET"])
def get_all_cupcakes():
    '''Return JSON object containing all cupcakes
        i.e. {"cupcakes": [{id, flavor, size, etc.}, ...]}'''
    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]
    return jsonify(cupcakes=serialized)

@app.route("/api/cupcakes/<int:id>", methods=["GET"])
def list_single_cupcake(id):
    '''Given a valid id, returns a JSON object containing that 
    cupcake's data'''
    cupcake = Cupcake.query.get_or_404(id)
    serialized = cupcake.serialize()
    return jsonify(cupcake=serialized)

@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.image = request.json.get("image", cupcake.image)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.size = request.json.get("size", cupcake.size)

    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    '''Adds a new cupcake to the database, and upon successful 
    creation, returns the JSON for that cupcake'''
    new_cupcake = Cupcake(**request.json)
    db.session.add(new_cupcake)
    db.session.commit()
    serialized = new_cupcake.serialize()
    print(serialized)
    return (jsonify(cupcake=serialized), 201)

@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify({"deleted": id})

@app.route("/", methods=["GET", "POST"])
def show_homepage():
    return render_template("base.html")



