from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.simple import StringField, TextAreaField, PasswordField, EmailField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class UserCreateForm(FlaskForm):
    username = StringField('이름', validators=[DataRequired('필수 입력 항목입니다.'), Length(min=3, max=25)])
    userid = StringField('아이디', validators=[DataRequired('필수 입력 항목입니다.'), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired('필수 입력 항목입니다.'), EqualTo('password2', message='비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호 확인', validators=[DataRequired('필수 입력 항목입니다.')])
    email = EmailField('이메일', validators=[DataRequired('필수 입력 항목입니다.'), Email()])
    Terms_of_Service = BooleanField('회원이용약관 동의 (필수)', validators=[DataRequired('필수 사항입니다.')])
    Privacy_Policy = BooleanField('개인정보처리방침 동의 (필수)', validators=[DataRequired('필수 사항입니다.')])
    receive_emails = BooleanField('이메일 수신 동의 (선택)')

class UserLoginForm(FlaskForm):
    userid = StringField('아이디', validators=[DataRequired('필수 입력 항목입니다.'), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired('필수 입력 항목입니다.')])

# 공지사항 리스트 폼 notice_list
class NoticeForm(FlaskForm):
    theater = StringField('영화관', validators=[DataRequired('전체')])
    subject = StringField('제목', validators=[DataRequired('제목은 필수 입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')])


class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')])