# seed.py
from datetime import datetime
from pybo import create_app, db
from pybo.models import Notice


def insert_test_data(n=12):
    """테스트용 질문 데이터 n개 생성"""
    app = create_app()  # Flask 컨텍스트 가 필요
    with app.app_context():
        years=[2025,2026]
        theaters=["강남스트리트점", "가산디지털점", "건대점", "용산점", "홍대점", "광교점", "부천점", "동탄점", "수원역점", "송도점", "인계점", "분당점", "양양점", "강릉점", "천안점", "오송점", "대전성심당점", "논산훈련소점", "광주점", "익산점", "전주점", "대구점", "포항점", "경주점", "울산점", "통영점", "김해점", "부산갈매기점", "제주점", "서귀포점"]

        for year in years:
            for i in range(n):
                for theater in theaters:
                    q = Notice(
                        theater=theater,
                        title=f'{theater} {year}년 {i + 1}월 휴무일 안내',
                        content=f'''안녕하세요, 필름아티크입니다. 
먼저 필름아티크 {theater}을 이용해주시는 고객님들께 항상 깊은 감사 드립니다.
                        
필름아티크 {theater}은 G7스퀘어 건물 전체 의무 휴업일에 따라
{i+1}월 9일(월)과 {i + 1}월 23일(월) 휴관합니다.
그 외 모든 요일은 정상 영업 예정이오니 이용에 참고 부탁 드립니다.
                              
※ 의무 휴업 기준 : 제 2018-243호 대형마트 및 준대규모점포 의무휴업일 지정 및 영업시간 제한 고시
                
감사합니다.''',

                        created_date=datetime(year, i+1, 1)
                    )
                    db.session.add(q)

        db.session.commit()
        print(f'{n}개의 테스트 데이터가 생성되었습니다.')

if __name__ == '__main__':
    insert_test_data()


