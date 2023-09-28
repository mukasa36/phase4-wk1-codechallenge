# Import SQLAlchemy and related modules
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.schema import CheckConstraint
from sqlalchemy import Table, Column, Integer, ForeignKey

# Create a SQLAlchemy database instance
db = SQLAlchemy()

# Define the RestaurantPizza model
class RestaurantPizza(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)

    # Add a check constraint to ensure the price is between 1 and 30
    _table_args_ = (CheckConstraint('price >= 1 AND price <= 30'),)

# Define the Restaurant model
class Restaurant(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)

    # Define the relationship between Restaurant and Pizza using a secondary table
    pizzas = db.relationship('Pizza', secondary='restaurant_pizza', back_populates='restaurants')

# Define the Pizza model
class Pizza(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)

    # Define the relationship between Pizza and Restaurant using a secondary table
    restaurants = db.relationship('Restaurant', secondary='restaurant_pizza', back_populates='pizzas')

# Define a many-to-many relationship table between Restaurant and Pizza
restaurant_pizza = Table(
    'restaurant_pizza',
    Column('restaurant_id', Integer, ForeignKey('restaurant.id'), primary_key=True),
    Column('pizza_id', Integer, ForeignKey('pizza.id'), primary_key=True),
)
