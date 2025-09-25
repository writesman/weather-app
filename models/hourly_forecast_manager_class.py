import csv
from .hourly_forecast_class import HourlyForecast


class HourlyForecastManager:
    """
    A manager class to load and store all hourly forecast data from a CSV file.
    It also stores the forecast generation time and the forecast URL.
    """

    def __init__(self, csv_file: str, generated_at: str) -> None:
        self.csv_file = csv_file
        self.generated_at = generated_at
        self.forecasts: list[HourlyForecast] = []

    def load_forecasts(self) -> bool:
        try:
            with open(self.csv_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.forecasts = [HourlyForecast.from_dict(row) for row in reader]
            return True
        except Exception as e:
            print(f"Error loading hourly forecasts: {e}")
            return False

    def get_forecasts(self) -> list[HourlyForecast]:
        return self.forecasts

