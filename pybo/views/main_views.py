from flask import Blueprint, render_template
from pybo.models import Movie, imgs

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    movies = Movie.query.limit(10).all()  # 슬라이드 개수
    first_movie = movies[0] if movies else None
    images = imgs.query.filter_by(img_type='main').all()
    logo_1 = imgs.query.filter_by(img_name='메인 로고1').first()
    logo_2 = imgs.query.filter_by(img_name='메인 로고2').first()
    main_1 = imgs.query.filter_by(img_name='메인 슬라이더1').first()
    main_2 = imgs.query.filter_by(img_name='메인 슬라이더2').first()
    main_3 = imgs.query.filter_by(img_name='메인 슬라이더3').first()
    event_1 = imgs.query.filter_by(img_name='메인 이벤트1').first()
    event_2 = imgs.query.filter_by(img_name='메인 이벤트2').first()
    event_3 = imgs.query.filter_by(img_name='메인 이벤트3').first()
    event_4 = imgs.query.filter_by(img_name='메인 이벤트4').first()
    event_5 = imgs.query.filter_by(img_name='메인 이벤트5').first()
    event_6 = imgs.query.filter_by(img_name='메인 이벤트6').first()
    screen_1 = imgs.query.filter_by(img_name='메인 스크린1').first()
    screen_2 = imgs.query.filter_by(img_name='메인 스크린2').first()
    screen_3 = imgs.query.filter_by(img_name='메인 스크린3').first()
    icon_1 = imgs.query.filter_by(img_name='메인 아이콘1').first()
    icon_2 = imgs.query.filter_by(img_name='메인 아이콘2').first()
    icon_3 = imgs.query.filter_by(img_name='메인 아이콘3').first()
    icon_4 = imgs.query.filter_by(img_name='메인 아이콘4').first()
    icon_5 = imgs.query.filter_by(img_name='메인 아이콘5').first()
    
    banner = imgs.query.filter_by(img_name='메인 배너1').first()


    return render_template(
        'main.html',
        movies=movies, 
        first_movie=first_movie, 
        images=images,
        logo_1=logo_1,
        logo_2=logo_2,
        main_1=main_1,
        main_2=main_2,
        main_3=main_3,
        event_1=event_1,
        event_2=event_2,
        event_3=event_3,
        event_4=event_4,
        event_5=event_5,
        event_6=event_6,
        screen_1=screen_1,
        screen_2=screen_2,
        screen_3=screen_3,
        icon_1=icon_1,
        icon_2=icon_2,
        icon_3=icon_3,
        icon_4=icon_4,
        icon_5=icon_5,
        banner=banner
        )