from datetime import datetime, date
import uuid, random, json

from flask import Blueprint, flash, jsonify, render_template, request, abort, jsonify, session, redirect, url_for
from pybo import db
from pybo.views.auth_views import login_required, g
from pybo.models import Movie, Payment, Schedule, Screen, Theater, User, Reservation, Order, imgs, Seat

from sqlalchemy import func
import requests, base64
from collections import defaultdict

bp = Blueprint('film', __name__, url_prefix='/film')

# 마이페이지
@bp.route('/mypage', methods=['GET'])
def mypage():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('auth.login'))

    user = User.query.get(user_id)

    from collections import defaultdict

    # 현재 예매 내역
    active = Reservation.query.filter_by(
        user_id=user.id,
        status='RESERVED'
    ).all()

    grouped = defaultdict(list)

    for r in active:
        grouped[r.schedule_id].append(r)

    reservation_list = []

    for schedule_id, items in grouped.items():
        schedule = items[0].schedule
        seats = [f"{i.seat.row}{i.seat.col}" for i in items]

        reservation_list.append({
            "schedule_id": schedule_id,
            "movie": schedule.movie.title,
            "theater": schedule.screen.theater.name,
            "datetime": schedule.start_time,
            "seats": ", ".join(seats)
        })

    # 취소 내역 (통합)
    cancels = []

    # 예매 취소
    canceled_reservations = Reservation.query.filter_by(
        user_id=user.id,
        status='CANCEL'
    ).all()

    cancel_group = defaultdict(list)

    for r in canceled_reservations:
        cancel_group[r.schedule_id].append(r)

    for schedule_id, items in cancel_group.items():
        schedule = items[0].schedule

        cancels.append({
            "type": "reservation",
            "movie_title": schedule.movie.title,
            "cancel_date": items[0].created_at.strftime("%Y-%m-%d %H:%M")
        })

    # 결제 취소
    cancel_payments = Payment.query\
        .join(Order)\
        .filter(
            Order.user_id == user.id,
            Payment.status == "CANCELLED"
        )\
        .all()

    for p in cancel_payments:
        cancels.append({
            "type": "payment",
            "movie_title": p.order.product_name,
            "cancel_date": p.approved_at.strftime("%Y-%m-%d %H:%M") if p.approved_at else "-"
        })

    # 결제 완료 내역
    payment = Payment.query\
        .join(Order)\
        .filter(
            Order.user_id == user.id,
            Payment.status == "SUCCESS"
        )\
        .all()

    orders = Order.query.filter_by(user_id=user.id).all()

    return render_template(
        'mypage.html',
        user=user,
        reservations=reservation_list,
        cancels=cancels,   
        payment=payment,
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
@login_required
def booking(movie_id):
    movies = Movie.query.all()

    # 선택된 영화
    movie = Movie.query.get(movie_id)

    if not movie:
        abort(404)
    # =====================================
    # 청소년관람불가 영화 성인인증 체크
    # =====================================
    cert = (movie.certification or '').strip()

    if cert in ['청소년관람불가', '청소년 관람불가', '청불', '19세', '19']:

        # 이미 인증 완료했는지 체크
        verified = session.get('adult_verified')

        if not verified:

            today = date.today()
            birth = g.user.birth

            age = today.year - birth.year

            if (today.month, today.day) < (birth.month, birth.day):
                age -= 1

            # 미성년자 차단
            if age < 19:
                flash('청소년 관람불가 영화는 성인만 예매 가능합니다.')
                return redirect(url_for('main.index'))

            # 성인인데 인증창 미통과 상태
            session['next_booking_url'] = request.url
            return redirect(url_for('film.adult_verify'))

    # =====================================

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

# ===============================
# 성인 인증 페이지
# ===============================
@bp.route('/adult_verify')
@login_required
def adult_verify():
    return render_template('adult_verify.html')


# ===============================
# 성인 인증 완료
# ===============================
@bp.route('/booking_pass')
@login_required
def booking_pass():

    session['adult_verified'] = True

    flash('성인 인증이 완료되었습니다.')

    return redirect(
        session.get(
            'next_booking_url',
            url_for('main.index')
        )
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
        reserved = len([r for r in s.reservations if r.status == 'RESERVED'])
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

@bp.route('/api/reserved_seats')
def reserved_seats():
    schedule_id = request.args.get('schedule_id', type=int)

    reservations = Reservation.query.filter_by(
        schedule_id=schedule_id,
        status='RESERVED'
        ).all()

    result = []

    for r in reservations:
        seat = r.seat
        seat_code = f"{seat.row}{seat.col}"
        result.append(seat_code)

    return jsonify(result)


@bp.route('/movie/payment', methods=['GET', 'POST'])
@login_required
def movie_payment():

    if request.method == 'POST':
        data = request.get_json()

        session['booking_data'] = data 

        return jsonify({"success": True})

    schedule_id = request.args.get('schedule_id', type=int)
    schedule = Schedule.query.get_or_404(schedule_id)

    movie = schedule.movie
    screen = schedule.screen
    theater = screen.theater

    
    payment_data = session.get('booking_data')
    if not payment_data:
        return redirect(url_for('film.person_seat', schedule_id=schedule.id))

    seats = payment_data.get('seats')
    people = payment_data.get('people')
    total_price = payment_data.get('total_price')

    num_people = sum(people.values())

    order_code = str(uuid.uuid4())

    order = Order(
    order_code=order_code,
    user_id=g.user.id,
    total_price=total_price,
    status='READY',

    
    seats_json=json.dumps(seats),
    people_json=json.dumps(people),
    schedule_id=schedule.id
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
        order=order, 
    )

@bp.route('/payment/success')
@login_required
def payment_success():

    order_id = request.args.get("order_id")

    if not order_id:
        return redirect(url_for('main.index'))

    order = Order.query.filter_by(order_code=order_id).first()

    if not order:
        return redirect(url_for('main.index'))

    seats = json.loads(order.seats_json)
    people = json.loads(order.people_json)
    schedule = Schedule.query.get(order.schedule_id)


    if order.status == "SUCCESS":
        return render_template(
            'payment_success.html',
            movie=schedule.movie,
            schedule=schedule,
            theater=schedule.screen.theater,
            screen=schedule.screen,
            seats=seats,
            total_price=order.total_price,
            people=people,
            booking_code=order.order_code
        )

    user_id = session.get('user_id')

    booking_code = order.order_code 
    order.status = "SUCCESS"

    reserved_seats = []

    for seat_code in seats:
        row = seat_code[0]
        col = int(seat_code[1:])

        seat = Seat.query.filter_by(
            screen_id=schedule.screen_id,
            row=row,
            col=col
        ).first()

        existing = Reservation.query.filter_by(
            schedule_id=schedule.id,
            seat_id=seat.id
        ).first()

        if existing:
            continue  

        reservation = Reservation(
            user_id=user_id,
            schedule_id=schedule.id,
            seat_id=seat.id,
            created_at=datetime.now()
        )

        db.session.add(reservation)
        reserved_seats.append(seat_code)

    db.session.commit()

    return render_template(
        'payment_success.html',
        movie=schedule.movie,
        schedule=schedule,
        theater=schedule.screen.theater,
        screen=schedule.screen,
        seats=seats,
        total_price=order.total_price,
        people=people,
        booking_code=booking_code
    )

@bp.route('/reservation/cancel/<int:schedule_id>', methods=['POST'])
def cancel_reservation(schedule_id):
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('auth.login'))

    reservations = Reservation.query.filter_by(
        user_id=user_id,
        schedule_id=schedule_id,
        status='RESERVED'   # ⭐ 이것도 추가
    ).all()

    for r in reservations:
        r.status = 'CANCEL'

    db.session.commit()
    flash('예매가 취소되었습니다.')

    return redirect(url_for('film.mypage'))