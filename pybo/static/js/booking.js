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


// 날짜 자동생성
const dateList = document.querySelector(".date ul");

const today = new Date();

for (let i = 0; i < 7; i++) {
  const date = new Date();
  date.setDate(today.getDate() + i);

  const day = date.getDate(); // 일
  const week = ["일", "월", "화", "수", "목", "금", "토"][date.getDay()];

  const li = document.createElement("li");

  li.innerHTML = `
    <span class="day">${day}</span>
    <span class="week">${week}</span>
  `;

  // 오늘 기본 선택
  if (i === 0) {
  li.classList.add("selected");
  }

  if (week === "토") li.style.color = "blue";
  if (week === "일") li.style.color = "red";


  dateList.appendChild(li);
}

// 날짜 선택
const dates = document.querySelectorAll(".date li");

dates.forEach(date => {
  date.addEventListener("click", () => {

    // 기존 선택 제거
    dates.forEach(d => d.classList.remove("selected"));

    // 선택
    date.classList.add("selected");

    // 🔥 추가된 부분
    const index = [...dates].indexOf(date);

    let times;

    if (index % 2 === 0) {
      times = generateTimes(8, 24);
    } else {
      times = generateTimes(9, 25);
    }

    renderTimes(times);
  });
});


//시간 선택
function generateTimes(startHour, endHour) {
  const times = [];

  let current = new Date();
  current.setHours(startHour, 0, 0, 0);

  const end = new Date();
  end.setHours(endHour, 0, 0, 0);

  while (current <= end) {
    const h = String(current.getHours()).padStart(2, "0");
    const m = String(current.getMinutes()).padStart(2, "0");

    times.push(`${h}:${m}`);

    current.setMinutes(current.getMinutes() + 150); // 2시간 30분
  }

  return times;
}

function renderTimes(times) {
  const timeList = document.querySelector(".time ul");
  timeList.innerHTML = "";

  // 🔥 관 먼저 돌림
  for (let screen = 1; screen <= 3; screen++) {

    // 🔥 관별 줄 구분용 div
    const row = document.createElement("div");
    row.classList.add("screen_row");

    times.forEach(time => {

      const li = document.createElement("li");

      const seats = Math.floor(Math.random() * 60);

      li.innerHTML = `
        <button class="time_btn ${seats === 0 ? "disabled" : ""}"
                data-time="${time}"
                data-screen="${screen}"
                ${seats === 0 ? "disabled" : ""}>
          
          ${screen}관 ${time}
          
          <span class="seat">
            ${seats === 0 ? "매진" : `잔여 ${seats}석`}
          </span>
        </button>
      `;

      row.appendChild(li);
    });

    timeList.appendChild(row); // 🔥 관 단위로 추가
  }
}


const timeListEl = document.querySelector(".time");

timeListEl.addEventListener("click", (e) => {
  const btn = e.target.closest(".time_btn");
  if (!btn) return;

  // 기존 선택 제거
  document.querySelectorAll(".time_btn").forEach(b => {
    b.classList.remove("selected");
  });

  
  // 선택
  btn.classList.add("selected");

  // console.log("선택된 시간:", btn.childNodes[0].textContent.trim());
});

renderTimes(generateTimes(8, 24));