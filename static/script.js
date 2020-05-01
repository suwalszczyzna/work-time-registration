const burger = document.querySelector(".menubar__burger");
const nav = document.querySelector(".menubar__menu");

burger.addEventListener("click", () => {
  burger.classList.toggle("burger-active");
  nav.classList.toggle("menu-active");
});
