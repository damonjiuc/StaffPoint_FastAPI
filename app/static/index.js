const swiper = new Swiper('.nets-swiper', {
    slidesPerView: 4, // сколько видно за раз
    spaceBetween: 40, // отступ между логотипами
    loop: true,       // бесконечная прокрутка
    autoplay: {
        delay: 2000,    // пауза между слайдами
        disableOnInteraction: false,
    },
    speed: 1000,      // скорость перехода
    grabCursor: true,
    breakpoints: {
        0: {           // всё до 767px
            slidesPerView: 1,
            spaceBetween: 20,
        },
        768: {         // планшеты
            slidesPerView: 3,
        },
        1024: {        // десктопы
            slidesPerView: 5,
        },
    },
});