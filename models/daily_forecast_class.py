from typing import Self
from utils.formatters import format_temperature, format_precipitation_probability


class DailyForecast:
    """
    A class representing a single daily forecast period with formatted data.
    Stores:
      - period_name (e.g. "Tonight" or "Tomorrow")
      - temperature_fahrenheit (e.g. "88°F")
      - temperature_celsius (e.g. "31.1°C")
      - precipitation_probability (e.g. "💧0%" or "💧50%")
      - icon_url "picture from api.weather.gov"
      - detailed_forecast
    """

    def __init__(self, period_name: str, temperature_fahrenheit: str, temperature_celsius: str,
                 precipitation_probability: str, weather_icon_url: str, detailed_forecast: str) -> None:
        self.period_name = period_name
        self.temperature_fahrenheit = temperature_fahrenheit
        self.temperature_celsius = temperature_celsius
        self.precipitation_probability = precipitation_probability
        self.weather_icon_url = weather_icon_url
        self.detailed_forecast = detailed_forecast

    @classmethod
    def from_dict(cls, forecast_dict: dict[str, str]) -> Self:
        temperature_value = forecast_dict.get("temperature", "")
        temperature_unit = forecast_dict.get("temperature_unit", "")
        temperature_celsius, temperature_fahrenheit = format_temperature(temperature_value, temperature_unit)

        precipitation_probability = format_precipitation_probability(forecast_dict.get('precipitation_probability_value', ""))

        return cls(
            period_name=forecast_dict.get("period_name", "N/A"),
            temperature_fahrenheit=temperature_fahrenheit,
            temperature_celsius=temperature_celsius,
            precipitation_probability=precipitation_probability,
            weather_icon_url=forecast_dict.get("weather_icon_url", "N/A"),
            detailed_forecast=forecast_dict.get("detailed_forecast", "N/A")
        )
