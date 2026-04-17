import requests

#관람 등급
def get_certification(tmdb_id):

    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/release_dates"
    params = {
        "api_key": "85a24c607dac1e0d9139a903ee0f509b"
    }

    res = requests.get(url, params=params)
    data = res.json()

    for country in data['results']:
        if country['iso_3166_1'] == 'KR':
            for release in country['release_dates']:
                cert = release['certification']
                if cert:  # 빈값 아닌 것만
                    return cert

    return "정보없음"

# 출연배우
def get_actors(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/credits"
    params = {
        "api_key": "85a24c607dac1e0d9139a903ee0f509b",
        "language": "ko-KR"
    }

    res = requests.get(url, params=params)
    data = res.json()

    actors = [cast['name'] for cast in data['cast'][:3]]  # 상위 3명
    return ", ".join(actors)


#장르
def get_genres(genre_ids):
    genre_map = {
        28: "액션",
        12: "모험",
        16: "애니메이션",
        35: "코미디",
        80: "범죄",
        18: "드라마",
        14: "판타지",
        27: "공포",
        10749: "로맨스",
        878: "SF"
    }

    return ", ".join([genre_map.get(g, "") for g in genre_ids])

def save_movies():
    from pybo.models import Movie, db

    url = "https://api.themoviedb.org/3/movie/now_playing"
    params = {
        "api_key": "85a24c607dac1e0d9139a903ee0f509b",
        "language": "ko-KR",
        "region" : "KR"
    }

    res = requests.get(url, params=params)
    data = res.json()

    for m in data['results']:
        if not Movie.query.filter_by(tmdb_id=m['id']).first():

            certification = get_certification(m['id'])
            genres = get_genres(m['genre_ids'])
            actors = get_actors(m['id']) 
            
            movie = Movie(
                tmdb_id=m['id'],
                title=m['title'],
                overview=m['overview'],
                poster_path=m['poster_path'],
                release_date=m['release_date'],
                vote_average=m['vote_average'],
                certification=certification,
                genres=genres,
                actors=actors
            )
            db.session.add(movie)

    db.session.commit()