from flask import Blueprint, render_template

bp = Blueprint('main', __name__, template_folder='templates')

@bp.route('')
@bp.route('/index')
def index():
    return render_template('home.html', title='Home')
