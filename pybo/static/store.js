const navItems = document.querySelectorAll("#nav ul li");
const sections = document.querySelectorAll("#sub_tit1, #sub_tit2, #sub_tit3");

// ease-out 스크롤 함수
function smoothScrollTo(targetY, duration = 200) {
    const startY = window.scrollY;
    const distance = targetY - startY;
    const startTime = performance.now();

    function easeOutCubic(t) {
        return 1 - Math.pow(1 - t, 3);
    }

    function scrollStep(currentTime) {
        const time = Math.min(1, (currentTime - startTime) / duration);
        const eased = easeOutCubic(time);

        window.scrollTo(0, startY + distance * eased);

        if (time < 1) {
            requestAnimationFrame(scrollStep);
        }
    }

    requestAnimationFrame(scrollStep);
}

// 클릭 이벤트
navItems.forEach((li) => {
    li.addEventListener("click", function(e) {
        e.preventDefault();

        const targetId = this.getAttribute("data-target");
        const target = document.querySelector(targetId);

        // ease-out 적용된 스크롤 실행
        smoothScrollTo(target.offsetTop - 70, 10);

        // active 처리
        navItems.forEach(item => item.classList.remove("active"));
        this.classList.add("active");
    });
});

// 스크롤 시 active 유지
window.addEventListener("scroll", () => {
    let currentSection = null;
    let minDistance = Infinity;

    sections.forEach(section => {
        const rect = section.getBoundingClientRect();
        const distance = Math.abs(rect.top);

        if (distance < minDistance) {
            minDistance = distance;
            currentSection = section;
        }
    });

    navItems.forEach(li => li.classList.remove("active"));

    if (currentSection) {
        const id = "#" + currentSection.id;
        navItems.forEach(li => {
            if (li.getAttribute("data-target") === id) {
                li.classList.add("active");
            }
        });
    }
});