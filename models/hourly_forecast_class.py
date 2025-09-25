from typing import Self
from utils import format_start_time, format_temperature, format_precipitation_probability, \
    format_dewpoint, format_relative_humidity, format_wind


class HourlyForecast:
    """
    A class representing a single hourly forecast period with formatted data.
    Stores:
      - date (e.g. Monday, Apr 28")
      - time (e.g. "10:00 AM"
      - temperature_fahrenheit (e.g. "75.0°F" or "N/A")
      - temperature_celsius (e.g. "23.9°C" or "N/A")
      - precipitation_probability (formatted with an emoji, e.g. "💧20%")
      - dewpoint_fahrenheit (e.g. "55.0°F" or "N/A")
      - dewpoint_celsius (e.g. "12.8°C" or "N/A")
      - relative_humidity (combined value and unit, e.g. "60%" or "N/A")
      - wind (combined wind speed and direction, e.g. "10 mph NW" or "N/A")
      - weather_emoji (e.g. "⛅" or "⛈️")
      - short_forecast (e.g. "Sunny" or "Mostly Cloudy")
    """

    def __init__(self, date: str, time: str, temperature_fahrenheit: str, temperature_celsius: str,
                 precipitation_probability: str, dewpoint_fahrenheit: str, dewpoint_celsius: str,
                 relative_humidity: str, wind: str, weather_emoji: str, short_forecast: str) -> None:
        self.date = date
        self.time = time
        self.temperature_fahrenheit = temperature_fahrenheit
        self.temperature_celsius = temperature_celsius
        self.precipitation_probability = precipitation_probability
        self.dewpoint_fahrenheit = dewpoint_fahrenheit
        self.dewpoint_celsius = dewpoint_celsius
        self.relative_humidity = relative_humidity
        self.wind = wind
        self.weather_emoji = weather_emoji
        self.short_forecast = short_forecast

    @classmethod
    def from_dict(cls, forecast_dict: dict[str, str]) -> Self:
        date, time = format_start_time(forecast_dict.get("start_time", ""))

        temperature_value = forecast_dict.get("temperature", "")
        temperature_unit = forecast_dict.get("temperature_unit", "")
        temperature_celsius, temperature_fahrenheit = format_temperature(temperature_value, temperature_unit)

        precipitation_probability = format_precipitation_probability(forecast_dict.get('precipitation_probability_value', ""))

        dewpoint_value = forecast_dict.get("dewpoint_value", "")
        dewpoint_unit = forecast_dict.get("dewpoint_unit", "")
        dewpoint_celsius, dewpoint_fahrenheit = format_dewpoint(dewpoint_value, dewpoint_unit)

        relative_humidity = format_relative_humidity(forecast_dict.get("relative_humidity_value", ""))

        wind_speed = forecast_dict.get("wind_speed", "")
        wind_direction = forecast_dict.get("wind_direction", "")
        wind = format_wind(wind_speed, wind_direction)

        weather_emoji = HourlyForecast.icon_url_to_emoji(forecast_dict.get("weather_icon_url", ""))


        return cls(
            date=date,
            time=time,
            temperature_fahrenheit=temperature_fahrenheit,
            temperature_celsius=temperature_celsius,
            precipitation_probability=precipitation_probability,
            dewpoint_fahrenheit=dewpoint_fahrenheit,
            dewpoint_celsius=dewpoint_celsius,
            relative_humidity=relative_humidity,
            wind=wind,
            weather_emoji=weather_emoji,
            short_forecast=forecast_dict.get("short_forecast", "")
        )

    @staticmethod
    def icon_url_to_emoji(url: str) -> str:
        if not url:
            return "N/A"

        # Extract the condition part of the URL after the last '/' and before any query string
        base = url.split('?')[0]
        condition = base.split('/')[-1].lower().split(',')[0]

        # Mapping of conditions to emojis
        mapping = {
            "skc": "☀️",  # Fair/clear
            "few": "🌤️",  # A few clouds
            "sct": "⛅",  # Partly cloudy
            "bkn": "🌥️",  # Mostly cloudy
            "ovc": "☁️",  # Overcast
            "wind_skc": "🌬️",  # Fair/clear and windy
            "wind_few": "🌬️",  # A few clouds and windy
            "wind_sct": "🌬️",  # Partly cloudy and windy
            "wind_bkn": "🌬️",  # Mostly cloudy and windy
            "wind_ovc": "🌬️",  # Overcast and windy
            "snow": "❄️",  # Snow
            "rain_snow": "🌨️",  # Rain/snow
            "rain_sleet": "🌨️",  # Rain/sleet
            "snow_sleet": "🌨️",  # Snow/sleet
            "fzra": "🧊",  # Freezing rain
            "rain_fzra": "🧊",  # Rain/freezing rain
            "snow_fzra": "🧊",  # Freezing rain/snow
            "sleet": "🧊",  # Sleet
            "rain": "🌧️",  # Rain
            "rain_showers": "🌦️",  # Rain showers (high cloud cover)
            "rain_showers_hi": "🌦️",  # Rain showers (low cloud cover)
            "tsra": "⛈️",  # Thunderstorm (high cloud cover)
            "tsra_sct": "⛈️",  # Thunderstorm (medium cloud cover)
            "tsra_hi": "⛈️",  # Thunderstorm (low cloud cover)
            "tornado": "🌪️",  # Tornado
            "hurricane": "🌀",  # Hurricane conditions
            "tropical_storm": "🌀",  # Tropical storm conditions
            "dust": "🌪️",  # Dust
            "smoke": "💨",  # Smoke
            "haze": "🌫️",  # Haze
            "hot": "🔥",  # Hot
            "cold": "🧊",  # Cold
            "blizzard": "🌨️",  # Blizzard
            "fog": "🌁"  # Fog/mist
        }

        # Return the matching emoji or fallback if not found
        return mapping.get(condition, "❓")
