const API_KEY = "85a24c607dac1e0d9139a903ee0f509b";

fetch(`https://api.themoviedb.org/3/movie/now_playing?api_key=${API_KEY}&language=ko-KR&region=KR`)
  .then(res => res.json())
  .then(data => {
    const wrapper = document.querySelector(".posterSwiper .swiper-wrapper");

    // 기존 slide들 가져오기
    const slides = wrapper.querySelectorAll(".swiper-slide");

    data.results.forEach((movie, index) => {
      if (movie.poster_path && slides[index]) {

        const slide = slides[index];

        // img 생성
        const img = document.createElement("img");
        img.src = "https://image.tmdb.org/t/p/w500" + movie.poster_path;

        // 🔥 txtbox보다 위에 넣기
        slide.insertBefore(img, slide.firstChild);
      }
    });

    swiper.update();
  });