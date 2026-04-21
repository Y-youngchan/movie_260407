document.addEventListener("DOMContentLoaded", function () {

    // 상태
    const selectedSeats = [];

    // DOM
    const plusBtns = document.querySelectorAll(".plus");
    const minusBtns = document.querySelectorAll(".mins");
    const numBoxes = document.querySelectorAll(".basic_num");
    const priceBox = document.querySelector(".total_price");
    const seatArea = document.querySelector(".seatselect");

    const maxTotal = 8;

    // 가격표
    const prices = [20000, 12000, 7000, 5000];

    // 총 인원
    function getTotalPeople() {
        let total = 0;
        numBoxes.forEach(box => {
            total += parseInt(box.textContent);
        });
        return total;
    }

    // 총 금액
    function calculatePrice() {
        let totalPrice = 0;

        numBoxes.forEach((box, index) => {
            totalPrice += parseInt(box.textContent) * prices[index];
        });

        return totalPrice;
    }

    // UI 업데이트
    function updateUI() {
        const total = getTotalPeople();
        const totalPrice = calculatePrice();

        numBoxes.forEach((box, index) => {
            const count = parseInt(box.textContent);

            plusBtns[index].disabled = total >= maxTotal;
            minusBtns[index].disabled = count <= 0;
        });

        priceBox.innerHTML = totalPrice.toLocaleString() + "원";
    }

    // 좌석 동기화
    function syncSeatsWithPeople() {
        const totalPeople = getTotalPeople();

        if (selectedSeats.length > totalPeople) {

            const removeCount = selectedSeats.length - totalPeople;

            for (let i = 0; i < removeCount; i++) {
                const seatId = selectedSeats.pop();

                const seatEl = document.querySelector(`[data-seat="${seatId}"]`);
                if (seatEl) seatEl.classList.remove("selected");
            }
        }
    }

    // 증가
    plusBtns.forEach((btn, index) => {
        btn.addEventListener("click", () => {

            if (getTotalPeople() >= maxTotal) return;

            numBoxes[index].textContent =
                parseInt(numBoxes[index].textContent) + 1;

            updateUI();
            syncSeatsWithPeople();
        });
    });

    // 감소
    minusBtns.forEach((btn, index) => {
        btn.addEventListener("click", () => {

            let count = parseInt(numBoxes[index].textContent);
            if (count <= 0) return;

            numBoxes[index].textContent = count - 1;

            updateUI();
            syncSeatsWithPeople();
        });
    });

    // 좌석 생성
    const rows = ["A", "B", "C", "D", "E", "F"];
    const cols = 10;

    rows.forEach(row => {

        const rowDiv = document.createElement("div");
        rowDiv.classList.add("seat_row");

        const label = document.createElement("span");
        label.classList.add("row_label");
        label.innerText = row;

        rowDiv.appendChild(label);

        for (let i = 1; i <= cols; i++) {
            const seat = document.createElement("button");

            seat.classList.add("seat");
            seat.innerText = i;
            seat.dataset.seat = `${row}${i}`;

            rowDiv.appendChild(seat);
        }

        seatArea.appendChild(rowDiv);
    });

    // 좌석 선택 
    seatArea.addEventListener("click", (e) => {

        const seat = e.target.closest(".seat");
        if (!seat) return;

        if (seat.classList.contains("disabled")) return;

        const seatId = seat.dataset.seat;
        const totalPeople = getTotalPeople();

        // 인원 선택 안 했을 때
        if (totalPeople === 0) {
            alert("인원을 먼저 선택하세요");
            return;
        }

        // 선택 해제
        if (seat.classList.contains("selected")) {

            seat.classList.remove("selected");

            const index = selectedSeats.indexOf(seatId);
            if (index > -1) selectedSeats.splice(index, 1);

        } else {

            // 인원 초과 방지
            if (selectedSeats.length >= totalPeople) {
                alert(`좌석은 ${totalPeople}개까지만 선택 가능합니다`);
                return;
            }

            seat.classList.add("selected");
            selectedSeats.push(seatId);
        }

        console.log("좌석:", selectedSeats);
    });

    // 초기 실행
    updateUI();
});