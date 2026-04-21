from pybo import db

# notice
class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theater = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    # user = db.relationship('User', backref=db.backref('answer_set'))
    # modify_date = db.Column(db.DateTime(), nullable=True)

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
    Terms_of_Service = db.Column(db.Boolean, nullable=False)
    Privacy_Policy = db.Column(db.Boolean, nullable=False)
    receive_emails = db.Column(db.Boolean, nullable=True, default='False')


# 공지사항 - FAQ
class Faq(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(100), nullable=False)
    question = db.Column(db.String(200), nullable=False)
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

    product = db.relationship('Product')
    user = db.relationship('User')

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    payment_key = db.Column(db.String(200))
    status = db.Column(db.String(20))  # SUCCESS / FAIL
    paid_at = db.Column(db.DateTime)

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
    user_id = db.Column(db.Integer)
    screening_id = db.Column(db.Integer)
    seat_id = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=False)
    seat_id = db.Column(db.Integer, db.ForeignKey('seat.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    schedule = db.relationship('Schedule', back_populates='reservations')
    seat = db.relationship('Seat', back_populates='reservations')
    user = db.relationship('User', backref=db.backref('reservations', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<Reservation {self.user_id} {self.schedule_id}>'

# 1대1 문의 - review __공자사항
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100), nullable=False)
    info = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    image_path = db.Column(db.Text(), nullable=True)
    create_date = db.Column(db.DateTime(), nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    # user = db.relationship('User', backref=db.backref('answer_set'))
    # modify_date = db.Column(db.DateTime(), nullable=True)