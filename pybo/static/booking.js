const regions = document.querySelectorAll(".region_list li");
const theaters = document.querySelectorAll(".theater_list li");
const movies = document.querySelectorAll(".movie li");

// 지역 선택
regions.forEach(region => {
  region.addEventListener("click", () => {

    const selected = region.innerText;

    // 지역 active
    regions.forEach(r => r.classList.remove("active"));
    region.classList.add("active");

    // 영화관 필터
    theaters.forEach(t => {
      t.style.display =
        t.dataset.region === selected ? "block" : "none";
    });

  });
});

// 지역에 따른 영화관 선택
theaters.forEach(theater => {
  theater.addEventListener("click", () => {

    // 기존 선택 제거
    theaters.forEach(t => t.classList.remove("selected"));

    // 클릭한 극장 선택
    theater.classList.add("selected");

  });
});

//영화 선택
movies.forEach(movie => {
  movie.addEventListener("click", () => {

    // 기존 선택 제거
    movies.forEach(m => m.classList.remove("selected"));

    // 클릭한 극장 선택
    movie.classList.add("selected");

  });
});


// 영화리스트
const API_KEY = "85a24c607dac1e0d9139a903ee0f509b";

fetch(`https://api.themoviedb.org/3/movie/now_playing?api_key=${API_KEY}&language=ko-KR&region=KR`)
  .then(res => res.json())
  .then(async data => {

    const titleList = document.querySelectorAll(".movie_title");

    // 영화 리스트 반복 (li 개수만큼)
    for (let i = 0; i < titleList.length; i++) {

      const movie = data.results[i];
      if (!movie) break;

      // 🔥 한국 관람등급 가져오기
      const res = await fetch(`https://api.themoviedb.org/3/movie/${movie.id}/release_dates?api_key=${API_KEY}`);
      const dates = await res.json();

      const kr = dates.results.find(r => r.iso_3166_1 === "KR");

      let age = "ALL";

      if (kr && kr.release_dates.length > 0) {
        age = kr.release_dates[0].certification || "ALL";
      }

      let ageClass = "";

      if (age === "19") ageClass = "age-19";
      else if (age === "15") ageClass = "age-15";
      else if (age === "12") ageClass = "age-12";
      else ageClass = "age-all";

      // 값 넣기
      titleList[i].innerHTML = `
        <span class="movie_age ${ageClass}">${age}</span>
        ${movie.title}
      `;
    }
  });