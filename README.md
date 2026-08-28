# Weather Dashboard

A small Flask web application that looks up a city and displays its current weather and five-day forecast. Weather data is provided by the [Open-Meteo](https://open-meteo.com/) geocoding and forecast APIs.

## Features

- Search for weather by city name
- View current temperature, conditions, and wind speed
- View a five-day forecast
- Toggle temperatures between Celsius and Fahrenheit
- Apply a visual theme based on the current temperature

## Requirements

- Python 3.9 or newer

## Setup

1. Clone the repository and change into the project directory.
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows, activate it with:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run the application

Start the development server with:

```bash
python app.py
```

Open <http://127.0.0.1:5000> in a browser, enter a city name, and select **Get Weather**.

## API

The application exposes a weather endpoint:

```text
GET /api/weather?city=London
```

It returns JSON containing the resolved city, current conditions, and up to five daily forecast entries. The endpoint returns `400` when the city is missing, `404` when it cannot be found, and `502` when an upstream weather service is unavailable.

## Project structure

```text
.
├── app.py                 # Flask application and weather API
├── requirements.txt       # Python dependencies
└── static/
    ├── index.html         # Dashboard markup
    ├── script.js          # Client-side behavior
    └── style.css           # Dashboard styles and themes
```
