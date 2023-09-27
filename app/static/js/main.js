const inputs = document.querySelectorAll(".input-field");
const toggle_btn = document.querySelectorAll(".toggle");
const main = document.querySelector("main");
const bullets = document.querySelectorAll(".bullets span");
const images = document.querySelectorAll(".image");


inputs.forEach((inp) => {
  inp.addEventListener("focus", () => {
    inp.classList.add("active");
  });
  inp.addEventListener("blur", () => {
    if (inp.value != "") return;
    inp.classList.remove("active");
  });
});

toggle_btn.forEach((btn) => {
  btn.addEventListener("click", () => {
    main.classList.toggle("sign-up-mode");
  });
});

// function moveSlider() {
//   let index = this.dataset.value;

//   let currentImage = document.querySelector(`.img-${index}`);
//   images.forEach((img) => img.classList.remove("show"));
//   currentImage.classList.add("show");

//   const textSlider = document.querySelector(".text-group");
//   textSlider.style.transform = `translateY(${-(index - 1) * 2.8}rem)`;

//   bullets.forEach((bull) => bull.classList.remove("active"));
//   this.classList.add("active");
// }

// bullets.forEach((bullet) => {
//   bullet.addEventListener("click", moveSlider);
// });

let currentIndex = 0;

function moveSlider(event) {
  let index;

  if(event && this.dataset.value) {
    index = this.dataset.value;
    currentIndex = index;
  } else {
    currentIndex = (currentIndex % bullets.length) + 1;
    index = currentIndex;
  }

  let currentImage = document.querySelector(`.img-${index}`);
  images.forEach((img) => img.classList.remove("show"));
  currentImage.classList.add("show");

  const textSlider = document.querySelector(".text-group");
  textSlider.style.transform = `translateY(${-(index - 1) * 2.8}rem)`;

  bullets.forEach((bull) => bull.classList.remove("active"));
  document.querySelector(`[data-value='${index}']`).classList.add("active");
}


setInterval(moveSlider, 5000);

bullets.forEach((bullet) => {
  bullet.addEventListener("click", moveSlider);
});

// This function toggles the sign-up mode based on the URL hash
function handleHashChange() {
  if (window.location.hash === "#signup") {
      main.classList.add("sign-up-mode");
  } else if (window.location.hash === "#signin") {
      main.classList.remove("sign-up-mode");
  }
}

// Check the hash on page load and adjust UI accordingly
document.addEventListener("DOMContentLoaded", handleHashChange);

// Adjust UI when the URL hash changes
window.addEventListener("hashchange", handleHashChange);


