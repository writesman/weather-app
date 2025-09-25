from .temperature_conversion import celsius_to_fahrenheit, fahrenheit_to_celsius
from datetime import datetime


def format_temperature(temperature_value, temperature_unit):
    if not temperature_value or not temperature_unit:
        return "N/A", "N/A"

    try:
        temperature_value = float(temperature_value)
    except (ValueError, TypeError):
        return "N/A", "N/A"

    if temperature_unit == "C":
        temperature_celsius = f"{temperature_value:.1f}°C"
        temperature_fahrenheit = f"{celsius_to_fahrenheit(temperature_value):.0f}°F"
    else:
        temperature_celsius = f"{fahrenheit_to_celsius(temperature_value):.1f}°C"
        temperature_fahrenheit = f"{temperature_value:.0f}°F"

    return temperature_celsius, temperature_fahrenheit


def format_precipitation_probability(precipitation_probability_value):
    return f"💧{precipitation_probability_value or '0'}%"


def format_start_time(start_time: str):
    if not start_time:
        return "N/A", "N/A"

    try:
        dt = datetime.fromisoformat(start_time)
    except ValueError:
        return "N/A", "N/A"

    date = dt.strftime("%A, %b %d")  # e.g., "Wednesday, Feb 26"
    time = dt.strftime("%I:%M %p")  # e.g., "08:00 AM"

    return date, time


def format_dewpoint(dewpoint_value, dewpoint_unit):
    if not dewpoint_value or not dewpoint_unit:
        return "N/A", "N/A"

    try:
        dewpoint_value = float(dewpoint_value)
    except (ValueError, TypeError):
        return "N/A", "N/A"

    if dewpoint_unit == "wmoUnit:degC":
        dewpoint_celsius = f"{dewpoint_value:.1f}°C"
        dewpoint_fahrenheit = f"{celsius_to_fahrenheit(dewpoint_value):.0f}°F"
    else:
        dewpoint_celsius = f"{fahrenheit_to_celsius(dewpoint_value):.1f}°C"
        dewpoint_fahrenheit = f"{dewpoint_value:.0f}°F"

    return dewpoint_celsius, dewpoint_fahrenheit


def format_relative_humidity(relative_humidity_value):
    return f"{relative_humidity_value or '0'}%"


def format_wind(wind_speed, wind_direction):
    if not wind_speed and not wind_direction:
        return "N/A"

    return f"{wind_speed} {wind_direction}"
