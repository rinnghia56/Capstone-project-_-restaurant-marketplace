const searchForm = document.querySelector(".search-form-container");
const cart = document.querySelector(".shopping-cart-container");
const loginForm = document.querySelector(".login-form-container");
const navbar = document.querySelector(".header .navbar");


window.onscroll = () => {
    navbar.classList.remove("active");
};

const homeParallaxImg = document.querySelector(".home .home-parallax-img");
if(document.querySelector(".home")) {
document.querySelector(".home").onmousemove = (e) => {
    const x = (window.innerWidth - e.pageX * 2) / 90;
    const y = (window.innerHeight - e.pageY * 2) / 90;
    homeParallaxImg.style.transform = `translateX(${y}px) translateY(${x}px)`;
};

document.querySelector(".home").onmouseleave = () => {
    homeParallaxImg.style.transform = "translateX(0px) translateY(0px)";
};
}