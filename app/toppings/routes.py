from flask import render_template, Blueprint, request, redirect, url_for, flash

import constants
from app import db
from app.db_models import Toppings

bp = Blueprint('pizza-toppings', __name__, template_folder='templates')

TOPPINGS = ["Pepperoni", "Sausage", "Olives"]


@bp.route('/', methods=constants.http_verbs)
def view_pizza_toppings():
    if request.method == 'GET':
        toppings = Toppings.query.all()
        return render_template('pizza_toppings_list.html', len=len(toppings), TOPPINGS=toppings, title='Pizza Toppings')


@bp.route('/add-topping', methods=constants.http_verbs)
def save_topping():
    if request.method == 'POST':
        topping_name = request.form.get("top")
        quantity = request.form.get("amount")
        new_topping = Toppings(topping_name=topping_name, topping_qty=quantity)
        try:
            db.session.add(new_topping)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            return render_template("500.html", error=str(ex))
        return redirect(url_for('pizza-toppings.view_pizza_toppings'))


@bp.route('/update-topping/<topping_id>', methods=constants.http_verbs)
def update_topping(topping_id):
    if request.method == 'POST':
        new_topping_qty = request.form.get("new_amount")
        topping = db.session.query(Toppings).filter_by(id=topping_id).first()
        topping.topping_qty = new_topping_qty
        db.session.commit()
        return redirect(url_for('pizza-toppings.view_pizza_toppings'))


@bp.route('/delete-topping/<topping_id>', methods=constants.http_verbs)
def delete_topping(topping_id):
    if request.method == 'DELETE':
        topping = db.session.query(Toppings).filter_by(id=topping_id).first()
        db.session.delete(topping)
        db.session.commit()
        return "Deletion of topping successful."
