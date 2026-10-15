const STATUSES = ["open", "assigned", "in_progress", "done"];

function buildStepper() {
  const stepper = document.createElement("div");
  stepper.className = "stepper";
  STATUSES.forEach((status, i) => {
    const step = document.createElement("div");
    step.className = "step";
    step.innerHTML = `
      <div class="step-line"></div>
      <div class="step-dot">${i + 1}</div>
      <div class="step-label">${status.replace("_", " ")}</div>`;
    stepper.appendChild(step);
  });
  return stepper;
}

function setStepper(stepper, status) {
  const current = STATUSES.indexOf(status);
  stepper.querySelectorAll(".step").forEach((step, i) => {
    step.classList.toggle("done", i < current);
    step.classList.toggle("current", i === current);
  });
}
