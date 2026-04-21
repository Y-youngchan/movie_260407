from datetime import datetime

from flask import Blueprint, jsonify, render_template, request, abort, jsonify, session, redirect, url_for
from pybo import db
from pybo.models import Movie, Schedule, Screen, Theater, User, Reservation, Order

from sqlalchemy import func
import requests, base64

bp = Blueprint('film', __name__, url_prefix='/film')

# 마이페이지

@bp.route('/mypage', methods=['GET', 'POST'])
def mypage():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('auth.login'))

    user = User.query.get(user_id)

    reservations = Reservation.query.filter_by(user_id=user.id).all()
    orders = Order.query.filter_by(user_id=user.id).all()

    return render_template(
        'mypage.html',
        user=user,
        reservations=reservations,
        orders=orders
    )

@bp.route('/event', methods=['GET'])
def event():
    return render_template('event.html')

@bp.route('/movie/list', methods=['GET'])
def movie_list():
    movies = Movie.query.all()
    return render_template('movie_list.html', movies=movies)

@bp.route('/movie/<int:movie_id>', methods=['GET'])
def movie_info(movie_id):
    movie = Movie.query.filter_by(tmdb_id=movie_id).first()

    if not movie:
        abort(404)

    return render_template(
        'movie_info/movie_info_1.html',
        movie=movie,
        movie_id=movie.id 
    )

@bp.route('/booking/<int:movie_id>', methods=['GET'])
def booking(movie_id):
    movies = Movie.query.all()

    # 선택된 영화
    movie = Movie.query.get(movie_id)

    if not movie:
        abort(404)

    theaters = Theater.query.all()

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
        theaters=theaters,
        dates=dates,
        schedules=schedules,
        selected_date=selected_date
    )

@bp.route('/api/schedules')
def get_schedules():
    movie_id = request.args.get('movie_id', type=int)
    date_str = request.args.get('date')
    theater_id = request.args.get('theater_id', type=int)

    date = datetime.strptime(date_str, "%Y-%m-%d")

    schedules = Schedule.query.join(Screen).join(Theater).filter(
        Schedule.movie_id == movie_id,
        func.date(Schedule.start_time) == date.date(),
        Theater.id == theater_id  
    ).all()

    result = []

    for s in schedules:
        reserved = len(s.reservations)
        total = s.screen.total_seats

        result.append({
            "id": s.id,
            "time": s.start_time.strftime("%H:%M"),
            "screen": s.screen.name,
            "remaining_seats": total - reserved
        })

    return jsonify(result)

@bp.route('/person/seat', methods=['GET'])
def person_seat():
    schedule_id = request.args.get('schedule_id', type=int)

    if not schedule_id:
        abort(400)

    schedule = Schedule.query.get(schedule_id)

    if not schedule:
        abort(404)

    movie = schedule.movie
    screen = schedule.screen
    theater = screen.theater

    return render_template(
        'person_seat.html',
        schedule=schedule,
        movie=movie,
        screen=screen,
        theater=theater
    )
