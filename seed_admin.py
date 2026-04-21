from pybo import db
from pybo.models import User
from werkzeug.security import generate_password_hash


def seed_admin():

    admins = [
        {
            "userid": "admin",
            "username": "슈퍼관리자",
            "password": "1111",
            "email": "admin@test.com",
            "role": "super"
        },
        {
            "userid": "manager",
            "username": "운영관리자",
            "password": "1111",
            "email": "manager@test.com",
            "role": "manager"
        }
    ]

    for data in admins:

        user = User.query.filter_by(userid=data["userid"]).first()

        # 이미 있으면 role 수정
        if user:
            user.is_admin = True
            user.admin_role = data["role"]

        # 없으면 새로 생성
        else:
            user = User(
                userid=data["userid"],
                username=data["username"],
                password=generate_password_hash(data["password"]),
                email=data["email"],
                Terms_of_Service=True,
                Privacy_Policy=True,
                receive_emails=False,
                status='normal',
                is_admin=True,
                admin_role=data["role"]
            )

            db.session.add(user)

    db.session.commit()
    print("관리자 계정 생성/업데이트 완료")


if __name__ == "__main__":
    from pybo import create_app

    app = create_app()

    with app.app_context():
        seed_admin()