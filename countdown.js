// countdown.js
class Countdown extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this.isRunning = false;
    this.remainingTime = 0;
  }

  connectedCallback() {
    this.render();
    this.startButton = this.shadowRoot.getElementById("start");
    this.resetButton = this.shadowRoot.getElementById("reset");
    this.display = this.shadowRoot.getElementById("display");

    this.startButton.addEventListener("click", () => this.toggleCountdown());
    this.resetButton.addEventListener("click", () => this.resetCountdown());
  }

  render() {
    this.shadowRoot.innerHTML = `
      <div>
        <div id="display">00:00</div>
        <button id="start">Start</button>
        <button id="reset">Reset</button>
      </div>
    `;
  }

  setTime(seconds) {
    this.remainingTime = seconds;
    this.updateDisplay();
  }

  toggleCountdown() {
    if (this.isRunning) {
      this.stopCountdown();
    } else {
      this.startCountdown();
    }
  }

  startCountdown() {
    if (this.remainingTime > 0 && !this.isRunning) {
      this.isRunning = true;
      this.startButton.textContent = "Pause";
      this.tick();
    }
  }

  stopCountdown() {
    this.isRunning = false;
    this.startButton.textContent = "Start";
  }

  resetCountdown() {
    this.stopCountdown();
    this.setTime(0);
  }

  tick() {
    if (this.isRunning) {
      this.remainingTime--;
      this.updateDisplay();

      if (this.remainingTime > 0) {
        setTimeout(() => this.tick(), 1000);
      } else {
        this.stopCountdown();
        this.countdownFinished();
      }
    }
  }

  updateDisplay() {
    const minutes = Math.floor(this.remainingTime / 60);
    const seconds = this.remainingTime % 60;
    this.display.textContent = `${minutes.toString().padStart(2, "0")}:${seconds
      .toString()
      .padStart(2, "0")}`;
  }

  countdownFinished() {
    Streamlit.setComponentValue({ event: "finished" });
  }
}

customElements.define("countdown-timer", Countdown);

function sendValue(value) {
  Streamlit.setComponentValue(value);
}

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onRender(event) {
  const data = event.detail.args;
  const countdown = document.getElementById("countdown");

  if (data.command === "set_time") {
    countdown.setTime(data.seconds);
  } else if (data.command === "start") {
    countdown.startCountdown();
  } else if (data.command === "stop") {
    countdown.stopCountdown();
  } else if (data.command === "reset") {
    countdown.resetCountdown();
  }

  // After the component has finished rendering, call Streamlit to indicate
  // that the component is ready.
  Streamlit.setComponentReady();
}

// Attach our `onRender` function to Streamlit's render event.
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);
// Tell Streamlit we're ready to start receiving data. We won't get our
// first RENDER_EVENT until we call this function.
Streamlit.setComponentReady();
