document.addEventListener("DOMContentLoaded", function () {
    const plusBtn = document.querySelector(".plus");
    const minusBtn = document.querySelector(".mins");
    const numBox = document.querySelector(".basic_num");
    const priceBox = document.querySelector(".end_price");

    const price = productprice;
    const maxCount = Productlimit;
    const minCount = 1;

    // 초기 상태 설정
    updateUI(parseInt(numBox.textContent));

    // 수량 증가
    plusBtn.addEventListener("click", function () {
        let count = parseInt(numBox.textContent);

        if (count < maxCount) {
            count++;
            updateUI(count);
        }
    });

    // 수량 감소
    minusBtn.addEventListener("click", function () {
        let count = parseInt(numBox.textContent);

        if (count > minCount) {
            count--;
            updateUI(count);
        }
    });

    // UI 전체 업데이트 
    function updateUI(count) {
        numBox.textContent = count;

        // 가격 업데이트
        priceBox.innerHTML = (price * count).toLocaleString() + "<em>원</em>";

        // 버튼 비활성화 처리
        plusBtn.disabled = (count >= maxCount);
        minusBtn.disabled = (count <= minCount);
    }
});

// 사용방법 / 유의사항

const tabMenu = document.querySelectorAll('.tab_menu li');
const tabContent = document.querySelectorAll('.tabcontent');

// 초기 상태
tabContent.forEach((tc, i) => {
  tc.style.display = i === 0 ? 'block' : 'none';
});

tabMenu.forEach((tm, i) => {
  tm.addEventListener('click', () => {

    tabMenu.forEach(el => el.classList.remove('active'));
    tabContent.forEach(el => el.style.display = 'none');

    tm.classList.add('active');
    tabContent[i].style.display = 'block';

  });
});