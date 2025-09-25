from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QTextEdit, QLabel, QFrame, QPushButton, QHBoxLayout
from .colors import HIGHLIGHT_BACKGROUND, WIDGET_BACKGROUND, WINDOW_BACKGROUND
import sys


class HourlyForecastTab(QWidget):
    """A widget to display hourly forecast information."""

    def __init__(self, parent=None):
        """Initializes the UI components and layout for displaying hourly forecasts."""
        super().__init__(parent)

        self.setStyleSheet(f"background-color: {WIDGET_BACKGROUND}; border: none;")

        # Initialize main layout
        self.hourly_layout = QVBoxLayout(self)
        self.hourly_layout.setContentsMargins(0, 0, 0, 0)
        self.hourly_layout.setSpacing(3)

        # Create and configure the top section (scroll area for hourly forecast rows)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(f"""
            QScrollBar:vertical {{
                background: {WIDGET_BACKGROUND};
                width: 17px;
                margin-top: 5px;
                margin-right: 5px;
                margin-bottom: 5px;
                border: none;
            }}
            QScrollBar::handle:vertical {{
                background: {HIGHLIGHT_BACKGROUND};
                min-height: 50px;
                border-radius: 5px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                background: none;
                border: none;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """)

        # Create a container widget for the scroll area with a vertical layout
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(5, 5, 5, 5)
        self.scroll_layout.setSpacing(5)
        self.scroll_content.setLayout(self.scroll_layout)

        # Set the scroll content widget to the scroll area
        self.scroll_area.setWidget(self.scroll_content)

        # Create and configure the bottom section (text area for generated time)
        self.hourly_generated_time = QTextEdit()
        self.hourly_generated_time.setReadOnly(True)
        self.hourly_generated_time.setPlainText("")
        self.hourly_generated_time.setFixedHeight(37)
        self.hourly_generated_time.setStyleSheet("padding: 5px;")


        # Add all sections to the main layout
        self.hourly_layout.addWidget(self.scroll_area)
        self.hourly_layout.addWidget(self.hourly_generated_time)

    def update_data(self, hourly_forecast_generated_time, hourly_forecasts):
        # Clear existing rows in the scroll area
        self._clear_forecast_rows()

        forecast_date = ""

        # Add new forecast row to the scroll layout
        for forecast in hourly_forecasts:
            row = HourlyForecastRow()
            row.update_data(forecast)

            if forecast.date != forecast_date:
                forecast_date = forecast.date
                header_row = HourlyForecastHeaderRow()
                header_row.update_data(forecast_date)
                self.scroll_layout.addWidget(header_row)
            # Connect signal to show extra details
            # row.showMoreClicked.connect(self.update_detailed_forecast_label)
            self.scroll_layout.addWidget(row)

        # Update the generated time label
        self.hourly_generated_time.setPlainText(f"Hourly forecast generated at {hourly_forecast_generated_time}")

    def clear_data(self):
        self._clear_forecast_rows()
        self.hourly_generated_time.setPlainText("")

    def _clear_forecast_rows(self):
        """Clears all the rows currently in the scroll layout."""
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


class HourlyForecastHeaderRow(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        heading_font = QFont()
        heading_font.setPixelSize(20)

        self.setFont(heading_font)
        self.setText("")
        self.setContentsMargins(5, 5, 5, 5)

    def update_data(self, date):
        self.setText(date)


class HourlyForecastRow(QFrame):
    """A row widget to display hourly forecast data."""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize the UI components and set up the layout
        self.setStyleSheet(f"""
            HourlyForecastRow {{
                background-color: {WINDOW_BACKGROUND};
                border-radius: 4px;
            }}
            QLabel {{
                background-color: {WINDOW_BACKGROUND};
                padding: 4px;
            }}
        """)

        self.uniform_font = QFont()
        self.uniform_font.setPixelSize(20)

        if sys.platform.startswith(("win", "cygwin")):
            font_name = "Segoe UI Emoji"
        elif sys.platform.startswith("darwin"):
            font_name = "Apple Color Emoji"
        else:
            font_name = "Noto Color Emoji"

        self.icon_font = QFont(font_name)

        self.icon_font.setPixelSize(20)

        self.is_expanded = False

        # Main row widgets
        self.hour_label = QLabel("", self)
        self.icon_label = QLabel("", self)
        self.rain_label = QLabel("", self)
        self.temp_label = QLabel("", self)
        self.wind_label = QLabel("", self)
        self.show_more_button = QPushButton("+", self)
        self.show_more_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {WIDGET_BACKGROUND};
                border: none;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {HIGHLIGHT_BACKGROUND};
            }}
        """)

        # Set fixed widths for consistent spacing
        self.hour_label.setFixedWidth(110)
        self.icon_label.setFixedWidth(45)
        self.rain_label.setFixedWidth(100)
        self.temp_label.setFixedWidth(70)
        self.show_more_button.setFixedSize(30, 30)

        # Details section (initially hidden)
        self.details_widget = QWidget()
        self.details_widget.setVisible(False)
        self.details_layout = QVBoxLayout(self.details_widget)
        self.details_layout.setSpacing(0)  # Reduced from default
        self.details_layout.setContentsMargins(0, 0, 0, 0)

        # Detail labels
        self.detail_short_forecast = QLabel("", self.details_widget)
        self.detail_short_forecast.setWordWrap(True)
        self.detail_dewpoint = QLabel("", self.details_widget)
        self.detail_humidity = QLabel("", self.details_widget)

        # Set fonts
        for widget in [self.hour_label, self.rain_label, self.temp_label, self.wind_label, self.detail_short_forecast,
                      self.detail_dewpoint, self.detail_humidity]:
            widget.setFont(self.uniform_font)

        self.icon_label.setFont(self.icon_font)

        # Main layout setup
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(0)

        # Top row layout
        self.top_row = QHBoxLayout()
        self.top_row.setContentsMargins(0, 0, 5, 0)

        # Add widgets
        for widget in [self.hour_label, self.icon_label, self.rain_label, self.temp_label, self.wind_label,
                       self.show_more_button]:
            self.top_row.addWidget(widget)

        for widget in [self.detail_short_forecast, self.detail_dewpoint, self.detail_humidity]:
            self.details_layout.addWidget(widget)

        # Add to main layout
        self.main_layout.addLayout(self.top_row)
        self.main_layout.addWidget(self.details_widget)

        # Connect button
        self.show_more_button.clicked.connect(self.toggle_details)

    def toggle_details(self):
        """Toggle the visibility of the details section."""
        self.is_expanded = not self.is_expanded
        self.details_widget.setVisible(self.is_expanded)
        self.show_more_button.setText("-" if self.is_expanded else "+")

    def update_data(self, forecast):
        """Populate the row with forecast data"""
        self.hour_label.setText(forecast.time)
        self.icon_label.setText(forecast.weather_emoji)
        self.rain_label.setText(forecast.precipitation_probability)
        self.temp_label.setText(forecast.temperature_fahrenheit)
        self.wind_label.setText(forecast.wind)

        self.detail_short_forecast.setText(f"Short Forecast: {forecast.short_forecast}")
        self.detail_dewpoint.setText(f"Dewpoint: {forecast.dewpoint_fahrenheit}")
        self.detail_humidity.setText(f"Relative Humidity: {forecast.relative_humidity}")
