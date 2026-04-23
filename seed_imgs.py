from pybo import create_app, db
from pybo.models import imgs

app = create_app()

with app.app_context():
    imgs.query.delete()

    data = [
        imgs(img_name='메인 로고1', img_url='/static/img/filmatique_white.png', img_type='main'),
        imgs(img_name='메인 로고2', img_url='/static/img/filmatique_red.png', img_type='main'),
        imgs(img_name='메인 슬라이더1', img_url='/static/img/main_movie_slide_1.jpg', img_type='main'),
        imgs(img_name='메인 슬라이더2', img_url='/static/img/concrete.jpeg', img_type='main'),
        imgs(img_name='메인 슬라이더3', img_url='/static/img/The_Battleship_Island.jpg', img_type='main'),
        imgs(img_name='메인 슬라이더4', img_url='/static/img/main_movie_slide_2.png', img_type='main'),
        imgs(img_name='메인 슬라이더5', img_url='/static/img/main_movie_slide_3.jpg', img_type='main'),
        imgs(img_name='메인 이벤트1', img_url='/static/img/event1.jpg', img_type='main'),
        imgs(img_name='메인 이벤트2', img_url='/static/img/event2.jpg', img_type='main'),
        imgs(img_name='메인 이벤트3', img_url='/static/img/event3.jpg', img_type='main'),
        imgs(img_name='메인 이벤트4', img_url='/static/img/event4.jpg', img_type='main'),
        imgs(img_name='메인 이벤트5', img_url='/static/img/event5.jpg', img_type='main'),
        imgs(img_name='메인 이벤트6', img_url='/static/img/event6.jpg', img_type='main'),
        imgs(img_name='메인 스크린1', img_url='/static/img/screen1.jpg', img_type='main'),
        imgs(img_name='메인 스크린2', img_url='/static/img/screen2.jpg', img_type='main'),
        imgs(img_name='메인 스크린3', img_url='/static/img/screen3.jpg', img_type='main'),
        imgs(img_name='메인 아이콘1', img_url='/static/img/user.png', img_type='main'),
        imgs(img_name='메인 아이콘2', img_url='/static/img/ticket.png', img_type='main'),
        imgs(img_name='메인 아이콘3', img_url='/static/img/store.png', img_type='main'),
        imgs(img_name='메인 아이콘4', img_url='/static/img/notice.png', img_type='main'),
        imgs(img_name='메인 아이콘5', img_url='/static/img/movie.png', img_type='main'),
        imgs(img_name='메인 배너1', img_url='/static/img/banner_AD.jpg', img_type='main'),
        imgs(img_name='이벤트1', img_url='/static/img/main_event1.jpg', img_type='event', event_img='/static/img/main_event1_1.jpg'),
        imgs(img_name='이벤트2', img_url='/static/img/main_event2.jpg', img_type='event', event_img='/static/img/main_event2_1.jpg'),
        imgs(img_name='이벤트3', img_url='/static/img/main_event3.jpg', img_type='event', event_img='/static/img/main_event3_1.jpg'),
        imgs(img_name='이벤트4', img_url='/static/img/main_event4.jpg', img_type='event', event_img='/static/img/main_event4_1.jpg'),
        imgs(img_name='이벤트5', img_url='/static/img/main_event5.jpg', img_type='event', event_img='/static/img/main_event5_1.jpg'),
        imgs(img_name='이벤트6', img_url='/static/img/main_event6.jpg', img_type='event', event_img='/static/img/main_event6_1.jpg'),
        imgs(img_name='이벤트7', img_url='/static/img/main_event7.jpg', img_type='event', event_img='/static/img/main_event7_1.jpg'),
        imgs(img_name='이벤트8', img_url='/static/img/main_event8.jpg', img_type='event', event_img='/static/img/main_event8_1.jpg'),
        imgs(img_name='이벤트9', img_url='/static/img/main_event9.jpg', img_type='event', event_img='/static/img/main_event9_1.jpg'),
        imgs(img_name='이벤트10', img_url='/static/img/main_event10.jpg', img_type='event', event_img='/static/img/main_event10_1.jpg'),
        imgs(img_name='이벤트11', img_url='/static/img/main_event11.jpg', img_type='event', event_img='/static/img/main_event11_1.jpg'),
        imgs(img_name='이벤트12', img_url='/static/img/main_event12.jpg', img_type='event', event_img='/static/img/main_event12_1.jpg')
    ]

    db.session.add_all(data)
    db.session.commit()