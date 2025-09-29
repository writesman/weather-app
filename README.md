# Weather App

A desktop weather application built with Python and PyQt5 that provides daily and hourly forecasts using data from the National Weather Service (NWS) API.

---

## Features

- **Location Search:** Search for any location using the integrated geopy library with the Nominatim service.
- **Current Weather:** See the current temperature and a short forecast for the selected location.
- **Daily and Hourly Forecasts:** View detailed weather information in separate "Daily" and "Hourly" tabs.
- **Responsive UI:** The application uses a `QThread` to fetch weather data in the background, ensuring the user interface remains responsive.

---

## Project Structure

- `main.py`: The entry point for the application.
- `ui/`: Contains all the PyQt5 UI components, such as the main window, forecast tabs, and search widget.
- `services/`: Includes the `ForecastWorker` for fetching weather data and the `GeolocatorService` for location lookups.
- `models/`: Defines the data structures for daily and hourly forecasts (`DailyForecast`, `HourlyForecast`) and their manager classes.
- `utils/`: Contains helper functions for temperature conversion and data formatting.

---

## Requirements

- Python 3.7+
- The dependencies listed in `requirements.txt`

---

## Setup

1. Clone the repository:
2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

1. Run the main application file from your terminal:

    ```bash
    python main.py
    ```

2. Enter a location in the search bar and click **Search** or press **Enter**.
3. Confirm the location in the dialog box.
4. The application will then fetch and display the weather forecast for the confirmed location.

---

## Data Source

- **Geocoding (Location Search):** `geopy` library using the **Nominatim** service.
- **Weather Forecast:** The **National Weather Service (NWS) API** (`api.weather.gov`) is used to retrieve forecast data by geographical point.
