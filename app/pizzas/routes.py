from flask import Blueprint, render_template, request, redirect, url_for

import constants
from app import db
from app.db_models import Pizzas, Toppings

bp = Blueprint('pizzas', __name__, template_folder='templates')
toppingsDict = []


@bp.route('/', methods=constants.http_verbs)
def view_pizzas():
    if request.method == 'GET':
        pizzas = Pizzas.query.all()
        toppings = Toppings.query.all()
        # loop through db toppings value and deduct the amount in the toppings json
        if len(toppingsDict) > 0:
            for i in range(0, len(toppingsDict)):
                for j in range(0, len(toppings)):
                    if int(toppingsDict[i]['toppingId']) == toppings[j].id:
                        toppings[j].topping_qty = toppings[j].topping_qty - 1
        return render_template('pizzas_list.html', len=len(pizzas), pizzas=pizzas, toppings=toppings,
                               toppings_len=len(toppings), toppingsDict=toppingsDict,
                               toppingsDictLen=len(toppingsDict), title='Pizza Manager')


@bp.route('/add-topping/<topping_id>', methods=constants.http_verbs)
def new_pizza_toppings(topping_id):
    if request.method == 'PUT':
        topping = db.session.query(Toppings).filter_by(id=topping_id).first()
        toppingsDict.append({'toppingId': topping_id, 'toppingName': topping.topping_name})
        return "Successful Addition"


@bp.route('/remove-topping/<array_index>', methods=constants.http_verbs)
def remove_pizza_topping(array_index):
    if request.method == 'PUT':
        toppingsDict.pop(int(array_index))
        return "Successful Removal"


@bp.route('/add-pizza', methods=constants.http_verbs)
def save_pizza():
    if request.method == 'POST':
        pizza_name = request.form.get("pizza-name")
        new_pizza = Pizzas(pizza_name=pizza_name, pizza_toppings=toppingsDict)
        try:
            db.session.add(new_pizza)
            db.session.commit()
            # loop through toppings on the new pizza and update the toppings table
            for i in range(0, len(toppingsDict)):
                topping = db.session.query(Toppings).filter_by(id=toppingsDict[i]['toppingId']).first()
                topping.topping_qty = topping.topping_qty - 1
                db.session.commit()
            toppingsDict.clear()
        except Exception as ex:
            db.session.rollback()
            return render_template("500.html", error=str(ex))
        return redirect(url_for('pizzas.view_pizzas'))


@bp.route('/delete-pizza/<pizza_id>', methods=constants.http_verbs)
def delete_pizza(pizza_id):
    if request.method == 'DELETE':
        pizza = db.session.query(Pizzas).filter_by(id=pizza_id).first()
        db.session.delete(pizza)
        db.session.commit()
        return "Deletion of pizza successful."

