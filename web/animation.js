const image = document.getElementById("animationImage");
const counter = document.getElementById("stepCounter");
const previous = document.getElementById("previousButton");
const next = document.getElementById("nextButton");

let step = 1;

function showStep() {
  image.src = `img/quickhull_visuals/${step}.png`;
  image.alt = `Quickhull step ${step}`;
  counter.textContent = `${step} / 16`;
}

previous.addEventListener("click", () => {
  step = step === 1 ? 16 : step - 1;
  showStep();
});

next.addEventListener("click", () => {
  step = step === 16 ? 1 : step + 1;
  showStep();
});

showStep();
