// 지역 선택에 따른 영화관
// const regionButtons = document.querySelectorAll(".region button");
// const theaters = document.querySelectorAll(".theater li");

// regionButtons.forEach(btn => {
//   btn.addEventListener("click", () => {

//     const selectedRegion = btn.innerText;

//     // 선택 표시
//     regionButtons.forEach(b => b.classList.remove("selected"));
//     btn.classList.add("selected");

//     // 영화관 필터링
//     theaters.forEach(theater => {
//       if (theater.dataset.region === selectedRegion) {
//         theater.style.display = "block";
//       } else {
//         theater.style.display = "none";
//       }
//     });

//   });
// });


// --------------------------
const regions = document.querySelectorAll(".region_list li");
const theaters = document.querySelectorAll(".theater_list li");

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
