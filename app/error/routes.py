from flask import Blueprint, render_template

bp = Blueprint('error', __name__, template_folder='templates')


@bp.route('/error')
def error():
    return render_template('500.html', title='Error')
