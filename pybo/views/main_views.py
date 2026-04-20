from flask import Blueprint, render_template
from pybo.models import Movie

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    movies = Movie.query.limit(10).all()  # 슬라이드 개수
    first_movie = movies[0] if movies else None

    return render_template('main.html', movies=movies, first_movie=first_movie)