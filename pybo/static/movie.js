const API_KEY = "85a24c607dac1e0d9139a903ee0f509b";

fetch(`https://api.themoviedb.org/3/movie/popular?api_key=${API_KEY}&language=ko-KR`)
  .then(res => res.json())
  .then(data => {
    const wrapper = document.querySelector(".posterSwiper .swiper-wrapper");

    wrapper.innerHTML = ""; 

    data.results.forEach(movie => {
      if (movie.poster_path) {
        const slide = document.createElement("div");
        slide.classList.add("swiper-slide");

        const img = document.createElement("img");
        img.src = "https://image.tmdb.org/t/p/w500" + movie.poster_path;
        img.style.height = "100%";

        slide.appendChild(img);
        wrapper.appendChild(slide);
      }
    });

    swiper.update();
  });