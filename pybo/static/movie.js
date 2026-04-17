const API_KEY = "85a24c607dac1e0d9139a903ee0f509b";

fetch(movieInfoUrl)
  .then(res => res.json())
  .then(data => {
    const wrapper = document.querySelector(".posterSwiper .swiper-wrapper");

    // 기존 slide들 가져오기
    const slides = wrapper.querySelectorAll(".swiper-slide");
    const detail_btn = document.querySelectorAll(".detail");

    data.results.forEach((movie, index) => {
      if (movie.poster_path && slides[index]) {

        const slide = slides[index];
        const btn = detail_btn[index];

        // img 생성
        const img = document.createElement("img");
        img.src = "https://image.tmdb.org/t/p/w500" + movie.poster_path;
        btn.addEventListener('click', function() {
          location.href=`/film/movie/list/info/${movie.id}`
        })

        // 🔥 txtbox보다 위에 넣기
        slide.insertBefore(img, slide.firstChild);
      }
    });

    swiper.update();
  });