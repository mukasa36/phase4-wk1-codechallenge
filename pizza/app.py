# from config import config
# Import necessary modules
from flask import Flask, request, jsonify, abort
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from models import db, Restaurant, Pizza, RestaurantPizza

# Create a Flask application instance
app = Flask(__name__)

# Configure the database URI and disable modification tracking
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza_restaurant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Disable JSON compact mode
app.json.compact = False

# Initialize the migration engine
migrate = Migrate(app, db)

# Initialize the database with the Flask app instance
db.init_app(app)

# Define route for retrieving all restaurants
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    # Return a JSON response with restaurant data
    return jsonify([{'id': r.id, 'name': r.name, 'address': r.address} for r in restaurants])

# Define route for retrieving a specific restaurant by ID
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant is None:
        return jsonify({'error': 'Restaurant not found'}), 404
    # Return a JSON response with restaurant and associated pizza data
    pizzas = [{'id': p.id, 'name': p.name, 'ingredients': p.ingredients} for p in restaurant.pizzas]
    return jsonify({'id': restaurant.id, 'name': restaurant.name, 'address': restaurant.address, 'pizzas': pizzas})

# Define route for deleting a restaurant by ID
@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant is None:
        return jsonify({'error': 'Restaurant not found'}), 404
    try:
        # Attempt to delete the restaurant and handle IntegrityError if associated pizzas exist
        db.session.delete(restaurant)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Cannot delete restaurant with associated pizzas'}), 400
    # Return an empty response with status code 204 (No Content)
    return '', 204

# Define route for retrieving all pizzas
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    # Return a JSON response with pizza data
    return jsonify([{'id': p.id, 'name': p.name, 'ingredients': p.ingredients} for p in pizzas])

# Define route for creating a new restaurant-pizza association
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    # Check for missing data
    if price is None or pizza_id is None or restaurant_id is None:
        return jsonify({'errors': ['validation errors']}), 400

    try:
        # Attempt to create a new restaurant-pizza association
        restaurant_pizza = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
        db.session.add(restaurant_pizza)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'errors': ['validation errors']}), 400

    # Retrieve pizza data and return it in the response
    pizza = Pizza.query.get(pizza_id)
    return jsonify({'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients})

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, port=5555)
