from flask import Blueprint, render_template, request, abort
from pybo import db
from pybo.models import Movie, Schedule, Screen
from sqlalchemy import func
import requests, base64

bp = Blueprint('film', __name__, url_prefix='/film')

@bp.route('/event', methods=['GET'])
def event():
    return render_template('event.html')


# 스토어 결제
@bp.route('/store/pay', methods=['GET'])
def store_pay():
    product_id = request.args.get('product_id', type=int)

    products = {
        1: {
            "name": "일반 관람권(2D)",
            "price": 18000,
            "image": "img/redticket.png",
            "detail": "일반 관람권(2D) 1매"
        },

        2: {
            "name": "VIP 관람권",
            "price": 25000,
            "image": "img/blackticket.png",
            "detail": "VIP 관람권 1매"
        },

        3: {
            "name": "BEST COMBO 교환권",
            "price": 25000,
            "image": "img/BEST COMBO 교환권.png",
            "detail": "반반콤보 or 싱글스낵콤보 중 택1"
        }
    }

    product = products.get(product_id)

    if not product:
        abort(404)

    return render_template('store_pay.html', product=product)

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