# Weather App

### A desktop weather application built using Python and PyQt5 utilizing the NWS API.

---

## Features

- **Location Search:** Users can effortlessly search for any location worldwide using **geopy's Nominatim service**.
- **Dual Forecast Views:** Provides comprehensive visibility through dedicated tabs for **Daily** and **Hourly** forecasts.
- **Non-Blocking UI:** Data fetching is handled asynchronously via the **ForecastWorker QThread**, ensuring the **PyQt5** GUI remains responsive.
- **Data Serialization:** Fetched raw forecast data is processed, modeled (e.g., `DailyForecast`), and saved to CSV files.

---

## Project Structure

The codebase is organized following a clear Python desktop application pattern:

- `main.py` - Application entry point and PyQt5 setup.
- `services/` - Business logic for external interactions: `ForecastWorker` (API) and `GeolocatorService`.
- `ui/` - All PyQt5 widgets and UI components (e.g., `DailyForecastTab`, `LocationSearchWidget`).
- `models/` - Data structure classes (`DailyForecast`, `HourlyForecast`) and their corresponding manager classes.
- `utils/` - Helper functions for formatting data (e.g., `format_temperature`, `celsius_to_fahrenheit`).

---

## Setup

This project requires **Python 3** and the dependencies listed in `requirements.txt`.

### Steps

1. Clone the Repository
2. Install Dependencies

    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

Run the main application file from your terminal:

```bash
python main.py
```

### How to use the app

1. The main window will launch with the **Search** Bar at the top.
2. Enter the name of a city (e.g., "Austin, Texas") or a landmark, and click **Search** or press **Enter**.
3. Confirm the location in the dialog box.
4. The application will fetch data in the background, displaying the current temperature and the full daily and hourly forecasts in their respective tabs.

## Data Source

- **Geocoding (Location Search):** `geopy` library using the **Nominatim** service.
- **Weather Forecast:** The **National Weather Service (NWS) API** (`api.weather.gov`) is used to retrieve forecast data by geographical point.
