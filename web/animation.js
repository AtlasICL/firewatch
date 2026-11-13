
const image = document.getElementById("animationImage");
const counter = document.getElementById("stepCounter");
const previous = document.getElementById("previousButton");
const next = document.getElementById("nextButton");
const autoplayButton = document.getElementById("autoplayButton");

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

previous.addEventListener("click", () => {
  step = step === 1 ? 16 : step - 1;
  showStep();
});

next.addEventListener("click", nextStep);

autoplayButton.addEventListener("click", () => {
  if (timer) {
    clearInterval(timer);
    timer = null;
    autoplayButton.textContent = "Autoplay: OFF";
  } else {
    timer = setInterval(nextStep, 2000);
    autoplayButton.textContent = "Autoplay: ON";
  }
});

showStep();
timer = setInterval(nextStep, 2000);
