from flask import Blueprint, render_template

bp = Blueprint('film', __name__, url_prefix='/film')

@bp.route('/event', methods=['GET'])
def event():
    return render_template('event.html')

@bp.route('/store', methods=['GET'])
def store():
    return render_template('store.html')