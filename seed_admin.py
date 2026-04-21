from pybo import db
from pybo.models import User

def seed_admin():
    # admin 계정 존재 여부 확인
    admin = User.query.filter_by(userid='admin').first()

    # 이미 있으면 종료
    if admin:
        print('이미 admin 계정이 존재합니다.')
        return

    # admin 계정 생성
    admin = User(
        userid='admin',
        username='관리자',
        password=generate_password_hash('1234'),
        email='admin@test.com',
        Terms_of_Service=True,
        Privacy_Policy=True,
        receive_emails=False,
        status='normal',
        is_admin=True
    )

    db.session.add(admin)
    db.session.commit()

    print('관리자 계정 생성 완료!')
    print('아이디: admin')
    print('비밀번호: 1234')