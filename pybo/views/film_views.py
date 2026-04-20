from flask import Blueprint, render_template, request, abort
from pybo import db
from pybo.models import Movie, Schedule, Screen
from sqlalchemy import func
import requests, base64

bp = Blueprint('film', __name__, url_prefix='/film')

@bp.route('/event', methods=['GET'])
def event():
    return render_template('event.html')

@bp.route('/movie/list', methods=['GET'])
def movie_list():
    movies = Movie.query.all()
    return render_template('movie_list.html', movies=movies)

@bp.route('/movie/<int:movie_id>', methods=['GET'])
def movie_info(movie_id):
    movie = Movie.query.get(movie_id)
    return render_template('movie_info/movie_info_1.html', movie=movie)

@bp.route('/booking/<int:movie_id>', methods=['GET'])
def booking(movie_id):
    movies = Movie.query.all()

    # 선택된 영화
    movie = Movie.query.get(movie_id)

    if not movie:
        abort(404)

    # 날짜 리스트 (중복 제거)
    dates = db.session.query(
        func.date(Schedule.start_time)
    ).filter(
        Schedule.movie_id == movie.id
    ).distinct().all()

    # 기본 날짜 하나 선택 (첫 번째)
    selected_date = dates[0][0] if dates else None

    # 해당 날짜 시간들
    schedules = []
    if selected_date:
        schedules = Schedule.query.filter(
            Schedule.movie_id == movie.id,
            func.date(Schedule.start_time) == selected_date
        ).all()

    return render_template(
        'booking.html',
        movie_id=movie_id,
        movies=movies,
        movie=movie,
        dates=dates,
        schedules=schedules,
        selected_date=selected_date
    )

@bp.route('/person/seat', methods=['GET','POST'])
def person_seat():
    return render_template('person_seat.html')