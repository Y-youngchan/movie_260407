from flask import Blueprint, render_template
from pybo.models import Movie

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    movies = Movie.query.limit(10).all()  # 슬라이드 개수
    return render_template('main.html', movies=movies)