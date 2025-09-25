import csv
from geopy.location import Location
import requests
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal


class ForecastWorker(QThread):
    """A worker that fetches weather data in the background."""

    # This signal will tell the main program when we're done
    worker_finished = pyqtSignal(bool, str, str, str)

    def __init__(self, location: Location) -> None:
        super().__init__()
        self.location = location

    def run(self) -> None:
        """The main method that runs when the thread starts"""
        try:
            # Step 1: Get location info from the API
            latitude = round(self.location.latitude, 4)
            longitude = round(self.location.longitude, 4)
            location_url = f"https://api.weather.gov/points/{latitude},{longitude}"
            print(location_url)
            location_data = self._get_api_data(location_url)

            # Step 2: Get daily forecast
            daily_forecast_url = location_data["properties"]["forecast"]
            daily_forecast_data = self._get_api_data(daily_forecast_url)
            daily_forecast_generated_time = datetime.fromisoformat(
                daily_forecast_data["properties"].get("generatedAt")).astimezone().strftime("%B %d, %Y, %I:%M %p")
            self._save_daily_forecast(daily_forecast_data)

            # Step 3: Get hourly forecast
            hourly_forecast_url = location_data["properties"]["forecastHourly"]
            hourly_forecast_data = self._get_api_data(hourly_forecast_url)
            hourly_forecast_generated_time = datetime.fromisoformat(
                hourly_forecast_data["properties"].get("generatedAt")).astimezone().strftime("%B %d, %Y, %I:%M %p")
            self._save_hourly_forecast(hourly_forecast_data)

            # Step 4: Tell the main program we're done
            self.worker_finished.emit(
                True, "Forecast CSV files written", daily_forecast_generated_time, hourly_forecast_generated_time
            )
        except requests.exceptions.RequestException as e:
            self.worker_finished.emit(False, f"Forecast fetch failed: {str(e)}", "", "")
        except (KeyError, TypeError) as e:
            self.worker_finished.emit(False, f"Invalid API response format: {str(e)}", "", "")
        except (IOError, OSError) as e:
            self.worker_finished.emit(False, f"File save failed: {str(e)}", "", "")

    def _get_api_data(self, url: str) -> dict:
        """Helper method to get data from an API endpoint"""
        response = requests.get(url, headers={"Cache-Control": "no-cache", "Pragma": "no-cache"}, timeout=10)
        response.raise_for_status()  # Raises an error if request failed
        return response.json()

    def _save_daily_forecast(self, daily_forecast_data: dict) -> None:
        """Save daily forecast data to CSV"""
        daily_periods = daily_forecast_data["properties"]["periods"]
        with open('data/daily_forecast_data.csv', mode='w', newline='') as daily_file:
            # define headers
            writer = csv.DictWriter(daily_file, fieldnames=[
                "period_number", "period_name", "start_time", "temperature", "temperature_unit",
                "precipitation_probability_unit", "precipitation_probability_value", "wind_speed", "wind_direction",
                "weather_icon_url", "short_forecast", "detailed_forecast"
            ])

            # Write header row
            writer.writeheader()

            # Write each period's data
            for period in daily_periods:
                writer.writerow({
                    "period_number": period.get("number", ""),
                    "period_name": period.get("name", ""),
                    "start_time": period.get("startTime", ""),
                    "temperature": period.get("temperature", ""),
                    "temperature_unit": period.get("temperatureUnit", ""),
                    "precipitation_probability_unit": period.get("probabilityOfPrecipitation", {}).get("unitCode", ""),
                    "precipitation_probability_value": period.get("probabilityOfPrecipitation", {}).get("value", ""),
                    "wind_speed": period.get("windSpeed", ""),
                    "wind_direction": period.get("windDirection", ""),
                    "weather_icon_url": period.get("icon", ""),
                    "short_forecast": period.get("shortForecast", ""),
                    "detailed_forecast": period.get("detailedForecast", "")
                })

    def _save_hourly_forecast(self, hourly_forecast_data: dict) -> None:
        hourly_periods = hourly_forecast_data["properties"]["periods"]
        with open('data/hourly_forecast_data.csv', mode='w', newline='') as hourly_file:
            # define headers
            writer = csv.DictWriter(hourly_file, fieldnames=[
                "period_number", "start_time", "temperature", "temperature_unit", "precipitation_probability_unit",
                "precipitation_probability_value", "dewpoint_unit", "dewpoint_value", "relative_humidity_unit",
                "relative_humidity_value", "wind_speed", "wind_direction", "weather_icon_url", "short_forecast"
            ])

            # Write header row
            writer.writeheader()

            # Write each period's data
            for period in hourly_periods:
                writer.writerow({
                    "period_number": period.get("number", ""),
                    "start_time": period.get("startTime", ""),
                    "temperature": period.get("temperature", ""),
                    "temperature_unit": period.get("temperatureUnit", ""),
                    "precipitation_probability_unit": period.get("probabilityOfPrecipitation", {}).get("unitCode", ""),
                    "precipitation_probability_value": period.get("probabilityOfPrecipitation", {}).get("value", ""),
                    "dewpoint_unit": period.get("dewpoint", {}).get("unitCode", ""),
                    "dewpoint_value": period.get("dewpoint", {}).get("value", ""),
                    "relative_humidity_unit": period.get("relativeHumidity", {}).get("unitCode", ""),
                    "relative_humidity_value": period.get("relativeHumidity", {}).get("value", ""),
                    "wind_speed": period.get("windSpeed", ""),
                    "wind_direction": period.get("windDirection", ""),
                    "weather_icon_url": period.get("icon", ""),
                    "short_forecast": period.get("shortForecast", "")
                })
