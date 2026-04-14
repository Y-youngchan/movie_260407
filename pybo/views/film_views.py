from flask import Blueprint, render_template

bp = Blueprint('film', __name__, url_prefix='/film')

@bp.route('/event', methods=['GET'])
def event():
    return render_template('event.html')

@bp.route('/store', methods=['GET'])
def store():
    return render_template('store.html')

@bp.route('/movie/list', methods=['GET'])
def movie_list():
    return render_template('movie_list.html')

@bp.route('/booking', methods=['GET','POST'])
def booking():
    return render_template('booking.html')