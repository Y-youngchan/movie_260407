from pybo import db


class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theater = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    # user = db.relationship('User', backref=db.backref('answer_set'))
    # modify_date = db.Column(db.DateTime(), nullable=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid= db.Column(db.String(200), unique=True, nullable=False)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Terms_of_Service = db.Column(db.Boolean, nullable=True, server_default='1')
    # Privacy_Policy = db.Column(db.Boolean, nullable=True, server_default='1')
    # receive_emails = db.Column(db.Boolean, nullable=True, server_default='1')

    Terms_of_Service = db.Column(db.Boolean, nullable=False)
    Privacy_Policy = db.Column(db.Boolean, nullable=False)
    receive_emails = db.Column(db.Boolean, nullable=True, default=False)