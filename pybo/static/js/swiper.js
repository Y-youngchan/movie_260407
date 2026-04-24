
// Initialize Swiper
var swiper = new Swiper(".mainSwiper", {
        loop: true,
        navigation: {
          nextEl: ".mainSwiper .swiper-button-next",
          prevEl: ".mainSwiper .swiper-button-prev",
        },
    });



var swiper = new Swiper(".posterSwiper", {
      slidesPerView: 5,
      spaceBetween: 19,
      loop: true,
      navigation: {
          nextEl: ".poster .swiper-button-next",
          prevEl: ".poster .swiper-button-prev",
        },
    });

var swiper = new Swiper(".noticeSwiper", {
    direction: "vertical",
    slidesPerView: "auto",
    loop: true,
    autoplay: {
        delay: 2000,
    },
  });