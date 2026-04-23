from datetime import datetime

from alembic.autogenerate.compare import server_defaults
from sqlalchemy.orm import backref, relationship

from pybo import db

from datetime import datetime

# notice
class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theater = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)


# Answer-답변 창
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notice_id = db.Column(db.Integer, db.ForeignKey('notice.id', ondelete='CASCADE'))
    notice = db.relationship('Notice', backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid= db.Column(db.String(200), unique=True, nullable=False)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    birth = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    Terms_of_Service = db.Column(db.Boolean, nullable=False)
    Privacy_Policy = db.Column(db.Boolean, nullable=False)
    receive_emails = db.Column(db.Boolean, nullable=True, default='False')
    status = db.Column(db.String(20), nullable=False, default='normal', server_default='normal')
    is_admin = db.Column(db.Boolean, nullable=False, default=False, server_default='0')
    admin_role = db.Column(db.String(20), default='none')


# 공지사항 - FAQ
class Faq(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(100), nullable=False)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    # user = db.relationship('User', backref=db.backref('answer_set'))
    # modify_date = db.Column(db.DateTime(), nullable=True)
    
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Productname = db.Column(db.String(200), nullable=False)
    Producttype = db.Column(db.String(50), nullable=False) # 티켓, 스낵음료, 굿즈
    Productprice = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, default=0) #재고
    status = db.Column(db.String(20), default='normal')  # normal = 판매중, soldout = 품절
    Productdescription = db.Column(db.Text) # 구성품
    Productimage_url = db.Column(db.String(300))
    Productlimit = db.Column(db.Integer, nullable=False)
    Productdate = db.Column(db.String(120), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_name = db.Column(db.String)
    user_userid = db.Column(db.String)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product_name = db.Column(db.String)
    quantity = db.Column(db.Integer)
    total_price = db.Column(db.Integer)
    status = db.Column(db.String(20), default="READY")  # READY / SUCCESS / FAIL
    created_at = db.Column(db.DateTime, default=db.func.now())
    order_code = db.Column(db.String(100), unique=True)

    seats_json = db.Column(db.Text)
    people_json = db.Column(db.Text)
    schedule_id = db.Column(db.Integer)

    product = db.relationship('Product')
    user = db.relationship('User')

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    payment_key = db.Column(db.String(200), unique=True)
    order_code = db.Column(db.String(100)) # 주문 코드 (조회/로그용)
    method = db.Column(db.String(50))
    amount = db.Column(db.Integer)
    status = db.Column(db.String(20)) # READY / SUCCESS / FAIL
    requested_at = db.Column(db.DateTime, default=db.func.now())
    approved_at = db.Column(db.DateTime)

    order = db.relationship('Order')

# 영화
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer, unique=True)
    title = db.Column(db.String(200))
    overview = db.Column(db.Text)
    poster_path = db.Column(db.String(300))
    release_date = db.Column(db.String(20))
    vote_average = db.Column(db.Float)
    certification = db.Column(db.String(10))
    genres = db.Column(db.String(200))
    actors = db.Column(db.String(300))

    schedules = db.relationship('Schedule', back_populates='movie', cascade='all, delete-orphan')


# 지역/지점
class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    theaters = db.relationship('Theater', back_populates='region', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Region {self.name}>'


class Theater(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    address = db.Column(db.String(200))

    region = db.relationship('Region', back_populates='theaters')
    screens = db.relationship('Screen', back_populates='theater', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Theater {self.name}>'


class Screen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)   # ex) 1관
    total_seats = db.Column(db.Integer, nullable=False)

    theater = db.relationship('Theater', back_populates='screens')
    schedules = db.relationship('Schedule', back_populates='screen', cascade='all, delete-orphan')
    seats = db.relationship('Seat', back_populates='screen', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Screen {self.theater.name} {self.name}>'

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    screen_id = db.Column(db.Integer, db.ForeignKey('screen.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    movie = db.relationship('Movie', back_populates='schedules')
    screen = db.relationship('Screen', back_populates='schedules')
    reservations = db.relationship('Reservation', back_populates='schedule', cascade='all, delete-orphan')

    __table_args__ = (
        db.CheckConstraint('end_time > start_time', name='ck_schedule_time'),
        db.UniqueConstraint('screen_id', 'start_time', name='uq_schedule_screen_start'),
    )

    def __repr__(self):
        return f'<Schedule {self.movie.title} {self.screen.name} {self.start_time}>'

class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    screen_id = db.Column(db.Integer, db.ForeignKey('screen.id'), nullable=False)
    row = db.Column(db.String(5), nullable=False)
    col = db.Column(db.Integer, nullable=False)

    screen = db.relationship('Screen', back_populates='seats')
    reservations = db.relationship('Reservation', back_populates='seat', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Seat {self.screen.name} {self.row}{self.col}>'


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=False)
    seat_id = db.Column(db.Integer, db.ForeignKey('seat.id'), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='RESERVED')

    __table_args__ = (
        db.UniqueConstraint('schedule_id', 'seat_id', name='uq_schedule_seat'),
    )

    schedule = db.relationship('Schedule', back_populates='reservations')
    seat = db.relationship('Seat', back_populates='reservations')
    user = db.relationship('User', backref=db.backref('reservations', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<Reservation user={self.user_id}, schedule={self.schedule_id}, seat={self.seat_id}>'

# 1대1 문의 - review __공자사항
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cs_ask = db.Column(db.String(50), nullable=False)
    cs_place = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    image_path = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True)
    answer_review = db.Column(db.Text(), nullable=True)
    user = relationship("User", foreign_keys=[user_id])

       # 답변 작성 관리자
    answer_admin_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='SET NULL'),
        nullable=True
    )

    answer_admin = db.relationship(
        'User',
        foreign_keys=[answer_admin_id],
        backref='answered_reviews'
    )

    # 답변 작성일
    answer_create_date = db.Column(db.DateTime(), nullable=True)

    # 답변 수정일
    answer_modify_date = db.Column(db.DateTime(), nullable=True)

    # 답변 상태 (대기 / 완료)
    answer_status = db.Column(
        db.String(20),
        nullable=False,
        default='waiting',
        server_default='waiting'
    )


# 기타(메인 이미지와 이벤트 안에 이미지 저장)
class imgs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_name = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(300), nullable=False)
    img_type = db.Column(db.String(20), nullable=False) 
    event_img = db.Column(db.String(300), nullable=True)
    is_main = db.Column(db.Boolean, default=False)