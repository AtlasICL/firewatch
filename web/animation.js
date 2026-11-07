const image = document.getElementById("animationImage");
const counter = document.getElementById("stepCounter");
const previous = document.getElementById("previousButton");
const next = document.getElementById("nextButton");

let step = 1;

function showStep() {
  image.src = `img/quickhull_visuals/${step}.png`;
  image.alt = `Quickhull step ${step}`;
  counter.textContent = `${step} / 17`;
}

previous.addEventListener("click", () => {
  step = step === 1 ? 17 : step - 1;
  showStep();
});

next.addEventListener("click", () => {
  step = step === 17 ? 1 : step + 1;
  showStep();
});

showStep();
