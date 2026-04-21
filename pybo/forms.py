from tabnanny import check

import select
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, MultipleFileField
from wtforms.fields.choices import RadioField, SelectField
from wtforms.fields.simple import StringField, TextAreaField, PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class UserCreateForm(FlaskForm):
    username = StringField('이름', validators=[DataRequired('필수 입력 항목입니다.'), Length(min=3, max=25)])
    userid = StringField('아이디', validators=[DataRequired('필수 입력 항목입니다.'), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired('필수 입력 항목입니다.'),
    EqualTo('password2', message='비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호 확인', validators=[DataRequired('필수 입력 항목입니다.')])
    email = EmailField('이메일', validators=[DataRequired('필수 입력 항목입니다.'), Email()])
    phone = StringField('전화번호', validators=[DataRequired('필수 입력 항목입니다.'), Length(min=12, max=13)])
    birth = StringField('생년월일', validators=[DataRequired('필수 입력 항목입니다.'), Length(10)])
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

# 공지사항 review_detail(1:1문의)
class ReviewForm(FlaskForm):
    cs_ask = RadioField('문의유형', choices=[
        ('question', '문의'),
        ('suggestion', '건의'),
        ('praise', '칭찬'),
        ('complaint', '불만'),
        ('etc', '기타')], validators=[DataRequired('필수 입력 항목입니다')])

    cs_place = SelectField(
        '영화관',
        choices=[
            ('1', '강남스트리트점'), ('2', '가산디지털점'), ('3', '건대점'), ('4', '용산점'), ('5', '홍대점'),
            ('6', '광교점'), ('7', '부천점'), ('8', '동탄점'), ('9', '수원역점'), ('10', '송도점'),
            ('11', '인계점'), ('12', '분당점'), ('13', '양양점'), ('14', '강릉점'), ('15', '천안점'),
            ('16', '오송점'), ('17', '대전성심당점'), ('18', '논산훈련소점'), ('19', '광주점'), ('20', '익산점'),
            ('21', '전주점'), ('22', '대구점'), ('23', '포항점'), ('24', '경주점'), ('25', '울산점'),
            ('26', '통영점'), ('27', '김해점'), ('28', '부산갈매기점'), ('29', '제주점'), ('30', '서귀포점')
        ],
        validators=[DataRequired()])

    subject = StringField('제목', validators=[DataRequired("제목은 필수 입력 항목입니다.")])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')])

    # 길이 제한이 없는 Text 타입 사용
    image = MultipleFileField('이미지 업로드',
                              validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], message='이미지 파일만 업로드 가능합니다.')])
    submit = SubmitField('등록하기')


# 공지사항 질문에 대한 답변 저장 폼(1:1 문의 사항)
class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')])
