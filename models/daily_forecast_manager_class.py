import csv
from .daily_forecast_class import DailyForecast


class DailyForecastManager:
    """
    A manager class to load and store all daily forecast data from a CSV file.
    It also stores the forecast generation time and the forecast URL.
    """

    def __init__(self, csv_file: str, generated_at: str) -> None:
        self.csv_file = csv_file
        self.generated_at = generated_at
        self.forecasts: list[DailyForecast] = []

    def load_forecasts(self) -> bool:
        try:
            with open(self.csv_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.forecasts = [DailyForecast.from_dict(row) for row in reader]
            return True
        except Exception as e:
            print(f"Error loading daily forecasts: {e}")
            return False

    def get_forecasts(self) -> list[DailyForecast]:
        return self.forecasts
