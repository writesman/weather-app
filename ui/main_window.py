from PyQt5.QtWidgets import QWidget, QVBoxLayout
from services import ForecastWorker
from models import DailyForecastManager, HourlyForecastManager
from .colors import TEXT, WINDOW_BACKGROUND
from .current_weather import CurrentWeatherWidget
from .forecast_tabs import ForecastTabsWidget
from .forecast_heading import ForecastHeadingWidget
from .location_search import LocationSearchWidget


class WeatherMainWindow(QWidget):
    def __init__(self, parent=None):
        """Sets up the UI layout and widgets."""
        super().__init__(parent)

        self.setStyleSheet(f"background-color: {WINDOW_BACKGROUND}; color: {TEXT};")

        self.setFixedSize(600, 800)

        self.search_widget = LocationSearchWidget(self)
        self.search_widget.locationConfirmed.connect(self.handle_location_confirmed)
        self.heading_widget = ForecastHeadingWidget(self)
        self.current_weather_widget = CurrentWeatherWidget(self)
        self.forecast_tabs_widget = ForecastTabsWidget(self)

        # Main layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.search_widget)
        layout.addWidget(self.heading_widget)
        layout.addWidget(self.current_weather_widget)
        layout.addWidget(self.forecast_tabs_widget)

        self.setLayout(layout)

    def handle_location_confirmed(self, location):
        """Handles the location confirmation event."""
        self.heading_widget.update_data(location.address)

        # Start forecast worker thread
        self.worker = ForecastWorker(location)
        self.worker.worker_finished.connect(self.handle_forecast_result)
        self.worker.start()

    def handle_forecast_result(self, success, message, daily_generated_time, hourly_generated_time):
        """Handles the forecast result update."""
        print(message)
        if success:
            daily_manager = DailyForecastManager("data/daily_forecast_data.csv", daily_generated_time)
            hourly_manager = HourlyForecastManager("data/hourly_forecast_data.csv", hourly_generated_time)

            if daily_manager.load_forecasts() and hourly_manager.load_forecasts():
                daily_forecasts = daily_manager.get_forecasts()
                hourly_forecasts = hourly_manager.get_forecasts()
                self.current_weather_widget.update_data(hourly_forecasts[0].temperature_fahrenheit,
                                                        hourly_forecasts[0].short_forecast)
                self.forecast_tabs_widget.update_data(daily_generated_time, hourly_generated_time, daily_forecasts,
                                                      hourly_forecasts)
            else:
                self.heading_widget.clear_data()
                self.current_weather_widget.clear_data()
                self.forecast_tabs_widget.clear_data()
        else:
            # Data retrieval failed, update UI to show no data
            self.heading_widget.clear_data()
            self.current_weather_widget.clear_data()
            self.forecast_tabs_widget.clear_data()
