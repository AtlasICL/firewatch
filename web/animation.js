const image = document.getElementById("animationImage");
const counter = document.getElementById("stepCounter");
const previous = document.getElementById("previousButton");
const next = document.getElementById("nextButton");
const autoplayToggle = document.getElementById("autoplayToggle");

let step = 1;
let timer = null;

function showStep() {
  image.src = `img/quickhull_visuals/${step}.png`;
  image.alt = `Quickhull step ${step}`;
  counter.textContent = `${step} / 16`;
}

function nextStep() {
  step = step === 16 ? 1 : step + 1;
  showStep();
}

function stopAutoplay() {
  clearInterval(timer);
  timer = null;
  autoplayToggle.checked = false;
}

previous.addEventListener("click", () => {
  stopAutoplay();
  step = step === 1 ? 16 : step - 1;
  showStep();
});

next.addEventListener("click", () => {
  stopAutoplay();
  nextStep();
});

autoplayToggle.addEventListener("change", () => {
  if (autoplayToggle.checked) {
    timer = setInterval(nextStep, 2000);
  } else {
    stopAutoplay();
  }
});

showStep();
timer = setInterval(nextStep, 2000);
