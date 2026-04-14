const API_KEY = "85a24c607dac1e0d9139a903ee0f509b";

fetch(`https://api.themoviedb.org/3/movie/now_playing?api_key=${API_KEY}&language=ko-KR&region=KR`)
  .then(res => res.json())
  .then(data => {
    const boxes = document.querySelectorAll(".movie .box");

    data.results.slice(0, boxes.length).forEach((movie, index) => {
      const box = boxes[index];

      const rating = movie.vote_average
        ? movie.vote_average.toFixed(1)
        : "0.0";

      const imgSrc = movie.poster_path
        ? `https://image.tmdb.org/t/p/w500${movie.poster_path}`
        : "/static/no-image.png";

      box.innerHTML += `
        <img src="${imgSrc}" alt="${movie.title}">
        <h4>${movie.title}</h4>
        <p>${rating}</p>

        <div class="txtbox">
            <a href="#">예매하기</a>
            <a href="/movie/${movie.id}">상세보기</a>
        </div>
      `;
    });
  });