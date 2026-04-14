const navItems = document.querySelectorAll("#nav ul li");

navItems.forEach((li) => {
    li.addEventListener("click", function(e) {
        e.preventDefault();

        const targetId = this.getAttribute("data-target");
        const target = document.querySelector(targetId);

        const offsetTop = target.offsetTop;

        window.scrollTo({
            top: offsetTop,
            behavior: "smooth"
        });
    });
});