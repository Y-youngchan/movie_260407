document.addEventListener("DOMContentLoaded", function () {

    const menuList = document.querySelectorAll(".sidebar li[data-tab]");
    const panels = document.querySelectorAll(".tab_panel");

    menuList.forEach(menu => {
        menu.addEventListener("click", function () {

            const target = this.dataset.tab;

            // 메뉴 active 제거
            menuList.forEach(item => {
                item.classList.remove("active");
            });

            // 탭 숨기기
            panels.forEach(panel => {
                panel.classList.remove("show");
            });

            // 선택 메뉴 활성화
            this.classList.add("active");

            // 선택 탭 보이기
            document.getElementById(target).classList.add("show");

        });
    });

});