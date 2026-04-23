from pybo import create_app, db
from pybo.models import Screen, Seat

app = create_app()

with app.app_context():

    screens = Screen.query.all()

    if not screens:
        print("Screen 데이터 없음")
        exit()

    rows = ['A', 'B', 'C', 'D', 'E', 'F']
    cols = range(1, 11)  # 1~10

    for screen in screens:
        print(f"{screen.name} 좌석 생성 중...")

        for row in rows:
            for col in cols:

                # 중복 체크
                exists = Seat.query.filter_by(
                    screen_id=screen.id,
                    row=row,
                    col=col
                ).first()

                if exists:
                    continue

                seat = Seat(
                    screen_id=screen.id,
                    row=row,
                    col=col
                )

                db.session.add(seat)

    db.session.commit()
    print("좌석 생성 완료! (A~F / 1~10)")