from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.simple import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired('필수 입력 항목입니다.'), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired('필수 입력 항목입니다.'), EqualTo('password2', message='비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호 확인', validators=[DataRequired('필수 입력 항목입니다.')])
    email = EmailField('이메일', validators=[DataRequired('필수 입력 항목입니다.'), Email()])

class UserLoginForm(FlaskForm):
    username = StringField('아이디', validators=[DataRequired('필수 입력 항목입니다.'), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired('필수 입력 항목입니다.')])