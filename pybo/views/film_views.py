from datetime import datetime
import uuid

from flask import Blueprint, flash, jsonify, render_template, request, abort, jsonify, session, redirect, url_for
from pybo import db
from pybo.views.auth_views import login_required, g
from pybo.models import Movie, Schedule, Screen, Theater, User, Reservation, Order, imgs

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

@bp.route('/event')
def event():
    event_images = imgs.query.filter_by(img_type='event').all()
    event_1 = imgs.query.filter_by(img_name='이벤트1').first()
    event_2 = imgs.query.filter_by(img_name='이벤트2').first()
    event_3 = imgs.query.filter_by(img_name='이벤트3').first()
    event_4 = imgs.query.filter_by(img_name='이벤트4').first()
    event_5 = imgs.query.filter_by(img_name='이벤트5').first()
    event_6 = imgs.query.filter_by(img_name='이벤트6').first()
    event_7 = imgs.query.filter_by(img_name='이벤트7').first()
    event_8 = imgs.query.filter_by(img_name='이벤트8').first()
    event_9 = imgs.query.filter_by(img_name='이벤트9').first()
    event_10 = imgs.query.filter_by(img_name='이벤트10').first()
    event_11 = imgs.query.filter_by(img_name='이벤트11').first()
    event_12 = imgs.query.filter_by(img_name='이벤트12').first()

    return render_template(
        'event.html', 
        images=event_images,
        event_1=event_1,
        event_2=event_2,
        event_3=event_3,
        event_4=event_4,
        event_5=event_5,
        event_6=event_6,
        event_7=event_7,
        event_8=event_8,
        event_9=event_9,
        event_10=event_10,
        event_11=event_11,
        event_12=event_12
    )

@bp.route('/event/<string:img_name>')
def event_detail(img_name):
    # img = imgs.query.filter_by(img_type='event').all()
    event_img = imgs.query.filter_by(img_name=img_name).first()

    return render_template(
        'event_main.html',
        images=event_img

    )

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

@bp.route('/person/seat', methods=['GET', 'POST'])
@login_required
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

@bp.route('/movie/payment', methods=['GET', 'POST'])
@login_required
def movie_payment():

    if request.method == 'POST':
        data = request.get_json()
        session['payment_data'] = data
        return jsonify({"success": True})

    
    schedule_id = request.args.get('schedule_id', type=int)
    schedule = Schedule.query.get_or_404(schedule_id)

    movie = schedule.movie
    screen = schedule.screen
    theater = screen.theater

    payment_data = session.get('payment_data')
    if not payment_data:
        abort(400)

    seats = payment_data.get('seats')
    people = payment_data.get('people')
    total_price = payment_data.get('total_price')

    num_people = sum(people.values())

    
    order_code = str(uuid.uuid4())

    order = Order(
        order_code=order_code,
        user_id=g.user.id,
        total_price=total_price,
        status='pending'
    )

    db.session.add(order)
    db.session.commit()

    return render_template(
        'movie_payment.html',
        schedule=schedule,
        movie=movie,
        screen=screen,
        theater=theater,
        seats=seats,
        people=people,
        num_people=num_people,
        total_price=total_price,
        order=order
    )

@bp.route('/payment/success')
def payment_success():
    order_id = request.args.get("order_id")

    order = Order.query.filter_by(order_code=order_id).first()

    # ✅ 여기서 결제 검증 + 상태 변경
    order.status = "paid"

    db.session.commit()

    return render_template("payment_success.html", order=order)