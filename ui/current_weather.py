from .colors import WIDGET_BACKGROUND
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QSizePolicy, QLabel, QHBoxLayout


class CurrentWeatherWidget(QFrame):
    """Displays the current temperature and short forecast using HourlyForecastManager."""

    def __init__(self, parent=None):
        """Initializes UI components."""
        super().__init__(parent)

        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet(f"background-color: {WIDGET_BACKGROUND}; border: none; padding: 7px;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Configure current temperature label
        current_temp_font = QFont()
        current_temp_font.setPixelSize(30)
        current_temp_font.setBold(True)

        self.currentTempLabel = QLabel("", self)
        self.currentTempLabel.setFont(current_temp_font)
        self.currentTempLabel.setStyleSheet("background-color: transparent;")
        self.currentTempLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Configure short forecast label
        short_forecast_font = QFont()
        short_forecast_font.setPixelSize(30)

        self.shortForecastLabel = QLabel("", self)
        self.shortForecastLabel.setFont(short_forecast_font)
        self.shortForecastLabel.setStyleSheet("background-color: transparent;")
        self.shortForecastLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Layout setup
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.currentTempLabel)
        layout.addWidget(self.shortForecastLabel, alignment=Qt.AlignRight)

    def update_data(self, temperature, short_forecast):
        """Fetches and updates weather data."""
        self.currentTempLabel.setText(f"{temperature}")
        self.shortForecastLabel.setText(f"{short_forecast}")

    def clear_data(self):
        """Handles cases where no forecast data is available."""
        self.currentTempLabel.setText("")
        self.shortForecastLabel.setText("")
