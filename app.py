import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Represents a cafe with its attributes.
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


def cafe_to_dict(cafe):
    """Convert a Cafe instance to a dictionary."""
    return {
        "id": cafe.id,
        "name": cafe.name,
        "map_url": cafe.map_url,
        "img_url": cafe.img_url,
        "location": cafe.location,
        "seats": cafe.seats,
        "has_toilet": cafe.has_toilet,
        "has_wifi": cafe.has_wifi,
        "has_sockets": cafe.has_sockets,
        "can_take_calls": cafe.can_take_calls,
        "coffee_price": cafe.coffee_price,
    }


@app.route("/")
def home():
    """Render the main page."""
    return render_template("index.html")


@app.route("/random", methods=["GET"])
def get_random_cafe():
    """Return a random cafe from the database."""
    cafes = Cafe.query.all()
    if not cafes:
        return jsonify(error="No cafes found in the database.")
    random_cafe = random.choice(cafes)
    return jsonify(cafe=cafe_to_dict(random_cafe))


@app.route("/all", methods=["GET"])
def get_all_cafes():
    """Return all cafes from the database."""
    cafes = Cafe.query.all()
    if not cafes:
        return jsonify(error="No cafes found in the database.")
    return jsonify(cafes=[cafe_to_dict(cafe) for cafe in cafes])


@app.route("/add", methods=["POST"])
def add_cafe():
    """Add a new cafe to the database."""
    new_cafe = Cafe(
        name=request.form.get('name'),
        map_url=request.form.get('map_url'),
        img_url=request.form.get('img_url'),
        location=request.form.get('location'),
        seats=request.form.get('seats'),
        has_toilet=bool(request.form.get('toilet')),
        has_wifi=bool(request.form.get('wifi')),
        has_sockets=bool(request.form.get('sockets')),
        can_take_calls=bool(request.form.get('calls')),
        coffee_price=request.form.get('coffee_price')
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    """Update the coffee price of a specific cafe."""
    cafe = Cafe.query.get(cafe_id)
    if not cafe:
        return jsonify(error="No cafe found with that id.")
    cafe.coffee_price = request.args.get('new_price')
    db.session.commit()
    return jsonify(success="Successfully updated the price.")


@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def report_closed(cafe_id):
    """Delete a specific cafe from the database."""
    api_key = request.args.get('api_key')
    if api_key != "TopSecretAPIKey":
        return jsonify(error="Sorry, that's not allowed. Make sure you have the correct api_key.")
    cafe = Cafe.query.get(cafe_id)
    if not cafe:
        return jsonify(error="No cafe found with that id.")
    db.session.delete(cafe)
    db.session.commit()
    return jsonify(success="Successfully deleted the cafe.")


if __name__ == '__main__':
    app.run(debug=True)
