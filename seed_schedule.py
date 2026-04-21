from datetime import datetime, timedelta

from pybo import create_app, db
from pybo.models import Movie, Region, Theater, Screen, Schedule

# 기존 영화 데이터는 그대로 유지합니다.
# 이 스크립트는 새로운 지역/극장/상영관/상영시간 구조를 생성하고,
# 기존 Movie 테이블의 데이터를 활용해 Schedule을 추가합니다.

THEATERS_BY_REGION = {
    "서울": ["강남스트리트점", "가산디지털점", "건대점", "용산점", "홍대점"],
    "경기/인천": ["광교점", "부천점", "동탄점", "수원역점", "송도점", "인계점", "분당점"],
    "강원": ["양양점", "강릉점"],
    "충청/대전": ["천안점", "오송점", "대전성심당점", "논산훈련소점"],
    "전라/광주": ["광주점", "익산점", "전주점"],
    "경북/대구": ["대구점", "포항점", "경주점"],
    "경남/부산": ["울산점", "통영점", "김해점", "부산갈매기점"],
    "제주": ["제주점", "서귀포점"],
}

SCREENS_PER_THEATER = 3
MOVIES_PER_SCREEN = 20
DAYS_TO_SEED = 7  # 7일치 상영시간 생성
MOVIE_DURATION_MINUTES = 100
BREAK_MINUTES = 10
START_HOUR = 8


def get_or_create_region(name):
    region = Region.query.filter_by(name=name).first()
    if region is None:
        region = Region(name=name)
        db.session.add(region)
        db.session.flush()
    return region


def get_or_create_theater(name, region):
    theater = Theater.query.filter_by(name=name).first()
    if theater is None:
        theater = Theater(name=name, region=region, address=f"{region.name} {name} 주소")
        db.session.add(theater)
        db.session.flush()
    return theater


def get_or_create_screen(theater, name, total_seats=60):
    screen = Screen.query.filter_by(theater_id=theater.id, name=name).first()
    if screen is None:
        screen = Screen(theater=theater, name=name, total_seats=total_seats)
        db.session.add(screen)
        db.session.flush()
    return screen


def seed_regions_theaters_screens():
    for region_name, theater_names in THEATERS_BY_REGION.items():
        region = get_or_create_region(region_name)

        for theater_name in theater_names:
            theater = get_or_create_theater(theater_name, region)

            for i in range(1, SCREENS_PER_THEATER + 1):
                get_or_create_screen(theater, f"{i}관")

    db.session.commit()


def seed_schedules():
    movies = Movie.query.order_by(Movie.id).limit(MOVIES_PER_SCREEN).all()
    screens = Screen.query.order_by(Screen.id).all()

    base_date = datetime.now().replace(hour=START_HOUR, minute=0, second=0, microsecond=0)

    schedule_count = 0

    for screen in screens:
        for day_offset in range(DAYS_TO_SEED):

            # 🎯 하루 시작
            day_start = base_date + timedelta(days=day_offset)

            # 🎯 하루 마감 (다음날 02:30)
            day_end = (day_start + timedelta(days=1)).replace(hour=2, minute=30, second=0, microsecond=0)

            current_start = day_start

            movie_index = 0

            while current_start < day_end:

                movie = movies[movie_index % len(movies)]

                start_time = current_start
                end_time = start_time + timedelta(minutes=MOVIE_DURATION_MINUTES)

                # 🎯 끝나는 시간이 영업시간 넘으면 종료
                if end_time > day_end:
                    break

                existing = Schedule.query.filter_by(
                    screen_id=screen.id,
                    start_time=start_time
                ).first()

                if not existing:
                    schedule = Schedule(
                        movie_id=movie.id,
                        screen_id=screen.id,
                        start_time=start_time,
                        end_time=end_time,
                    )
                    db.session.add(schedule)
                    schedule_count += 1

                # 다음 영화 시간
                current_start = end_time + timedelta(minutes=BREAK_MINUTES)

                movie_index += 1

    db.session.commit()
    print(f"생성된 Schedule 데이터: {schedule_count}개")


def insert_test_data():
    app = create_app()
    with app.app_context():
        seed_regions_theaters_screens()
        seed_schedules()


if __name__ == '__main__':
    insert_test_data()