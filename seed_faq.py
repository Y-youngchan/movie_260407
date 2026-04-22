from datetime import datetime
from pybo import create_app, db
from pybo.models import Faq


def insert_test_data(n=6):
    """테스트용 질문 데이터 n개 생성"""
    app = create_app()  # Flask 컨텍스트 가 필요
    with app.app_context():
        kinds = ["영화관 이용", "관람권", "예매", "영화관 이용", "관람권", "예매"]
        questions = ['굿즈 상영기준은 어떻게 되나요?', '특별관 전용 관람권이 따로 있나요?', '영화 관람시간대 중 조조는 언제인가요?', '굿즈 상영기준은 어떻게 되나요?',
                     '특별관 전용 관람권이 따로 있나요?', '영화 관람시간대 중 조조는 언제인가요?']
        answers = [
            "굿즈 상영 기준은 영화사 정책에 따라 다릅니다.",
            "특별관 전용 관람권은 별도 구매가 필요합니다.",
            "조조는 보통 오전 6~10시입니다.",
            "굿즈 상영 기준은 영화사 정책에 따라 다릅니다.",
            "특별관 전용 관람권은 별도 구매가 필요합니다.",
            "조조는 보통 오전 6~10시입니다."

        ]

        for i in range(n):
            q = Faq(
                kind=kinds[i],
                question=questions[i],
                answer=answers[i],
                create_date=datetime.now()
            )
            db.session.add(q)
        db.session.commit()
        print(f"{n}개의 테스트 데이터가 생성되었습니다.")


if __name__ == '__main__':
    insert_test_data()
