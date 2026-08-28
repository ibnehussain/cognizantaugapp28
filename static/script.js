const cityInput = document.getElementById("cityInput");
const getWeatherBtn = document.getElementById("getWeatherBtn");
const unitToggleBtn = document.getElementById("unitToggleBtn");
const resultsEl = document.getElementById("results");
const errorEl = document.getElementById("error");
const cityNameEl = document.getElementById("cityName");
const tempEl = document.getElementById("temp");
const descriptionEl = document.getElementById("description");
const windEl = document.getElementById("wind");
const forecastStripEl = document.getElementById("forecastStrip");

let lastWeatherData = null; // cached Celsius payload from the API
let unit = "C";

getWeatherBtn.addEventListener("click", () => fetchWeather(cityInput.value.trim()));
cityInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") fetchWeather(cityInput.value.trim());
});
unitToggleBtn.addEventListener("click", () => {
  unit = unit === "C" ? "F" : "C";
  unitToggleBtn.textContent = `°${unit}`;
  if (lastWeatherData) render(lastWeatherData);
});

async function fetchWeather(city) {
  if (!city) return;

  hideError();

  try {
    const res = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || "Something went wrong");
    }

    lastWeatherData = data;
    render(data);
  } catch (err) {
    resultsEl.classList.add("hidden");
    showError(err.message || "Unable to fetch weather data");
  }
}

function render(data) {
  cityNameEl.textContent = `${data.city}, ${data.country}`;
  tempEl.textContent = formatTemp(data.current.temp, unit);
  descriptionEl.textContent = data.current.description;
  windEl.textContent = `Wind: ${data.current.windspeed} km/h`;

  forecastStripEl.innerHTML = "";
  data.daily.forEach((day) => {
    const card = document.createElement("div");
    card.className = "forecast-day";
    card.innerHTML = `
      <div class="day-label">${formatDay(day.date)}</div>
      <div>${day.description}</div>
      <div>${formatTemp(day.tempMax, unit)} / ${formatTemp(day.tempMin, unit)}</div>
    `;
    forecastStripEl.appendChild(card);
  });

  resultsEl.classList.remove("hidden");
}

function formatTemp(celsius, targetUnit) {
  const value = targetUnit === "F" ? (celsius * 9) / 5 + 32 : celsius;
  return `${Math.round(value)}°${targetUnit}`;
}

function formatDay(dateStr) {
  return new Date(dateStr).toLocaleDateString(undefined, { weekday: "short" });
}

function showError(message) {
  errorEl.textContent = message;
  errorEl.classList.remove("hidden");
}

function hideError() {
  errorEl.classList.add("hidden");
}
