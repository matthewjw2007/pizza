# File where data tables will be modeled
from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import JSONB

from app import db


# Pizza toppings table
class Toppings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topping_name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    topping_qty = db.Column(db.Integer, nullable=False)


# Pizza table
class Pizzas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pizza_name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    pizza_toppings = db.Column(JSON, nullable=False)
