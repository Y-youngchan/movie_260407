// 선택 상태
let selected = {
  theater: null,
  movie: null,
  date: null,
  schedule: null
};

// DOM
const regions = document.querySelectorAll(".region_list li");
const theaters = document.querySelectorAll(".theater_list li");
const movies = document.querySelectorAll(".movie li");
const dateList = document.querySelector(".date ul");
const timeList = document.querySelector(".time ul");

// 지역 선택
regions.forEach(region => {
  region.addEventListener("click", () => {

    const selectedRegion = region.innerText;

    regions.forEach(r => r.classList.remove("active"));
    region.classList.add("active");

    theaters.forEach(t => {
      t.style.display =
        t.dataset.region === selectedRegion ? "block" : "none";
    });
  });
});

// 극장 선택
theaters.forEach(theater => {
  theater.addEventListener("click", () => {

    theaters.forEach(t => t.classList.remove("selected"));
    theater.classList.add("selected");

    selected.theater = theater.dataset.theaterId;

    loadSchedules(); // 바로 호출
  });
});

// 영화 선택
movies.forEach(movie => {
  movie.addEventListener("click", () => {

    movies.forEach(m => m.classList.remove("selected"));
    movie.classList.add("selected");

    selected.movie = movie.dataset.movieId;

    loadSchedules(); // 바로 호출
  });
});


// 날짜 생성
const today = new Date();

for (let i = 0; i < 7; i++) {
  const date = new Date();
  date.setDate(today.getDate() + i);

  const day = date.getDate();
  const week = ["일", "월", "화", "수", "목", "금", "토"][date.getDay()];

  const li = document.createElement("li");

  li.innerHTML = `
    <span class="day">${day}</span>
    <span class="week">${week}</span>
  `;

  li.dataset.date = formatDate(date);

  if (i === 0) {
    li.classList.add("selected");
    selected.date = li.dataset.date;
  }

  if (week === "토") li.style.color = "blue";
  if (week === "일") li.style.color = "red";

  dateList.appendChild(li);
}

// 날짜 선택
document.addEventListener("click", (e) => {
  const date = e.target.closest(".date li");
  if (!date) return;

  document.querySelectorAll(".date li").forEach(d => {
    d.classList.remove("selected");
  });

  date.classList.add("selected");

  selected.date = date.dataset.date;

  loadSchedules(); // 🔥 핵심
});


// 날짜 포맷

function formatDate(date) {
  return date.toISOString().split("T")[0];
}


// 핵심 API 호출

function loadSchedules() {
  if (!selected.movie || !selected.date) return;

  fetch(`/film/api/schedules?movie_id=${selected.movie}&date=${selected.date}&theater_id=${selected.theater}`)
    .then(res => res.json())
    .then(data => renderTimes(data));
}

// 시간표 렌더링

function renderTimes(schedules) {

  timeList.innerHTML = "";

  if (schedules.length === 0) {
    timeList.innerHTML = "<li>상영시간 없음</li>";
    return;
  }

  // 관별 그룹화
  const grouped = {};

  schedules.forEach(s => {
    if (!grouped[s.screen]) grouped[s.screen] = [];
    grouped[s.screen].push(s);
  });

  // 렌더링
  Object.keys(grouped).forEach(screen => {

    const row = document.createElement("div");
    row.classList.add("screen_row");

    grouped[screen].forEach(s => {

      const li = document.createElement("li");

      const isSoldOut = s.remaining_seats <= 0;

      li.innerHTML = `
        <button class="time_btn ${isSoldOut ? "disabled" : ""}"
                data-schedule-id="${s.id}"
                ${isSoldOut ? "disabled" : ""}>
          
          ${screen} ${s.time}
          
          <span class="seat">
            ${isSoldOut ? "매진" : `잔여 ${s.remaining_seats}석`}
          </span>
        </button>
      `;

      row.appendChild(li);
    });

    timeList.appendChild(row);
  });
}


// 시간 선택

document.querySelector(".time").addEventListener("click", (e) => {

  const btn = e.target.closest(".time_btn");
  if (!btn) return;

  document.querySelectorAll(".time_btn").forEach(b => {
    b.classList.remove("selected");
  });

  btn.classList.add("selected");

  selected.schedule = btn.dataset.scheduleId;
});

// 좌석 이동

document.getElementById("btnSeats").addEventListener("click", (e) => {

  e.preventDefault();

  if (!selected.schedule) {
    alert("시간을 선택하세요");
    return;
  }

  location.href = `/film/person/seat?schedule_id=${selected.schedule}`;
});


// 초기 실행 (선택된 영화 있을 경우)

if (movieId) {
  selected.movie = movieId;
  loadSchedules();
}