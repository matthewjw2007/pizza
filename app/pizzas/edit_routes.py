import ast

from flask import Blueprint, request, render_template, redirect, url_for

import constants
from app import db
from app.db_models import Pizzas, Toppings

bp = Blueprint('edit-pizza', __name__, template_folder='templates')
newToppingsAdded = []
currentPizzaId = 0


@bp.route('/<pizza_id>', methods=constants.http_verbs)
def edit_pizza(pizza_id):
    if request.method == 'GET':
        currentPizzaId = pizza_id
        pizza = db.session.query(Pizzas).filter_by(id=pizza_id).first()
        current_toppings_len = len(pizza.pizza_toppings)
        available_toppings = Toppings.query.all()
        if len(newToppingsAdded) > 0:
            for i in range(0, len(newToppingsAdded)):
                for j in range(0, len(available_toppings)):
                    if int(newToppingsAdded[i]['toppingId']) == available_toppings[j].id:
                        available_toppings[j].topping_qty = available_toppings[j].topping_qty - 1
        return render_template('edit_pizza.html', pizza=pizza, current_toppings_len=current_toppings_len,
                               updated_toppings=newToppingsAdded, updated_toppings_len=len(newToppingsAdded),
                               available_toppings=available_toppings, available_toppings_len=len(available_toppings),
                               current_pizza_id=currentPizzaId, title='Edit Pizza')


@bp.route('/add-topping/<topping_id>', methods=constants.http_verbs)
def new_pizza_toppings(topping_id):
    if request.method == 'PUT':
        topping = db.session.query(Toppings).filter_by(id=topping_id).first()
        newToppingsAdded.append({'toppingId': topping_id, 'toppingName': topping.topping_name})
        return "Successful Addition"


@bp.route('/remove-original-topping', methods=constants.http_verbs)
def remove_pizza_topping():
    if request.method == 'PUT':
        pizza_id = request.args.get('pizzaId')
        topping_id = request.args.get('toppingId')
        topping = db.session.query(Toppings).filter_by(id=topping_id).first()
        topping_removed = {'toppingId': topping_id, 'toppingName': topping.topping_name}
        pizza = db.session.query(Pizzas).filter_by(id=pizza_id).first()
        update_pizza_toppings = pizza.pizza_toppings
        update_pizza_toppings.remove(topping_removed)
        pizza.pizza_toppings = []
        db.session.commit()
        pizza.pizza_toppings = update_pizza_toppings
        db.session.commit()
        return "Successful Removal"


@bp.route('/remove-new-topping/<array_index>', methods=constants.http_verbs)
def remove_new_pizza_topping(array_index):
    if request.method == 'PUT':
        newToppingsAdded.pop(int(array_index))
        return "Successful Removal"


@bp.route('/update/<pizza_id>', methods=constants.http_verbs)
def update_pizza(pizza_id):
    if request.method == 'POST':
        new_pizza_name = request.form.get("pizza-name")
        pizza = db.session.query(Pizzas).filter_by(id=pizza_id).first()
        pizza.pizza_name = new_pizza_name
        current_pizza_toppings = pizza.pizza_toppings
        updated_toppings_list = current_pizza_toppings + newToppingsAdded
        pizza.pizza_toppings = updated_toppings_list
        try:
            db.session.commit()
            newToppingsAdded.clear()
        except Exception as ex:
            db.session.rollback()
            return render_template("500.html", error=str(ex))
        return redirect(url_for('pizzas.view_pizzas'))
