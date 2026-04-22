/*tab할시 다른 메뉴는 보이고 나머지는 숨기기*/
const tabMenu = document.querySelectorAll('.nav nav-underline');
        const tabContent = document.querySelectorAll('.nav-link');

        tabMenu.forEach((tm, i) => {
            tm.addEventListener('click', () => {
                // 모든 탭 메뉴에서 'active' 클래스 제거
                tabMenu.forEach(item => {
                    item.classList.remove('active');
                });

                // 클릭한 탭 메뉴에만 'active' 클래스 추가
                tm.classList.add('active');

                // 탭에 해당하는 리스트 보이고, 나머지는 숨기기
                tabContent.forEach((tc, j) => {
                    tc.style.display = (i === j) ? 'flex' : 'none';
                });
            });
        });

     // 페이지버튼 클릭시
 const page_elements = document.querySelectorAll('.page-link')
        console.log(page_elements)
        page_elements.forEach(element => {
            element.addEventListener('click', function () {
                const page = this.dataset.page;
                if (page) {
                    document.getElementById('page').value = page;
                    document.getElementById('searchForm').submit();
                }
            })
        })


const trs = document.querySelectorAll(".outside tbody > tr");
const select = document.getElementById("filter");

select.addEventListener("change", function () {
    const value = this.value;

    trs.forEach(tr => {
        const col1 = tr.children[0].innerText.trim();

        if (value === "전체" || col1 === value) {
            tr.style.display = "";
        }
        else {
            tr.style.display = "none";
        }
    });
});


function toggleFAQ(row) {
    const answerRow = row.nextElementSibling;

    if (answerRow && answerRow.classList.contains("faq-answer-row")) {
        answerRow.style.display =
            answerRow.style.display === "table-row" ? "none" : "table-row";
    }
}
