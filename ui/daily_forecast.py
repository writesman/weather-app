from PyQt5.QtCore import pyqtSignal, Qt, QUrl
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget, QScrollArea, QHBoxLayout, QTextEdit
from .colors import HIGHLIGHT_BACKGROUND, WIDGET_BACKGROUND, WINDOW_BACKGROUND


class DailyForecastTab(QWidget):
    """A widget to display daily forecast information, including forecast cards and detailed forecast."""

    def __init__(self, parent=None):
        """Initializes the UI components and layout for displaying daily forecasts."""
        super().__init__(parent)

        self.setStyleSheet(f"background-color: {WIDGET_BACKGROUND}; border: none;")

        # Initialize main layout
        self.daily_layout = QVBoxLayout(self)
        self.daily_layout.setContentsMargins(0, 0, 0, 0)
        self.daily_layout.setSpacing(3)

        # Create and configure the top section (scroll area for daily forecast cards)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(f"""
            QScrollBar:horizontal {{
                background: {WIDGET_BACKGROUND};
                height: 17px;
                margin-left: 5px;
                margin-right: 5px;
                margin-bottom: 5px;
                border: none;
            }}
            QScrollBar::handle:horizontal {{
                background: {HIGHLIGHT_BACKGROUND};
                min-width: 20px;
                border-radius: 5px;;
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                background: none;
                border: none;
            }}
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
                background: none;
            }}
        """)

        # Create a container widget for the scroll area with a horizontal layout
        self.scroll_content = QWidget()
        self.scroll_layout = QHBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(5, 5, 5, 5)
        self.scroll_layout.setSpacing(10)
        self.scroll_content.setLayout(self.scroll_layout)

        # Set the scroll content widget to the scroll area
        self.scroll_area.setWidget(self.scroll_content)

        # Create and configure the middle section (detailed forecast display area)
        self.detailed_forecast_label = QTextEdit()
        self.detailed_forecast_label.setReadOnly(True)
        self.detailed_forecast_label.setPlainText("")
        self.detailed_forecast_label.setFixedHeight(100)
        self.detailed_forecast_label.setStyleSheet(f"""
            QTextEdit {{
                padding: 5px;
            }}
            QScrollBar:vertical {{
                background: {WIDGET_BACKGROUND};
                width: 12px;
                margin: 0px;
                border: none;
            }}
            QScrollBar::handle:vertical {{
                background: {HIGHLIGHT_BACKGROUND};
                min-height: 20px;
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

        # Create and configure the bottom section (text area for generated time)
        self.daily_generated_time = QTextEdit()
        self.daily_generated_time.setReadOnly(True)
        self.daily_generated_time.setPlainText("")
        self.daily_generated_time.setFixedHeight(37)
        self.daily_generated_time.setStyleSheet("padding: 5px;")

        # Add all sections to the main layout
        self.daily_layout.addWidget(self.scroll_area)
        self.daily_layout.addWidget(self.detailed_forecast_label)
        self.daily_layout.addWidget(self.daily_generated_time)

    def update_data(self, daily_forecast_generated_time, daily_forecasts):
        """
        Loads and updates the daily forecast data.
        This will update the scroll area with new forecast cards and show the detailed forecast for the first item.
        """
        # Clear existing forecast cards in the scroll area
        self._clear_forecast_cards()

        # Add new forecast cards to the scroll layout
        for forecast in daily_forecasts:
            card = DailyForecastCard()
            card.update_data(forecast)
            # Connect signal to show detailed forecast
            card.showMoreClicked.connect(self.update_detailed_forecast_label)
            card.setFixedWidth(150)
            self.scroll_layout.addWidget(card)

        self.scroll_layout.addStretch()  # Stretch the layout to fill remaining space

        # Display the detailed forecast of the first forecast card
        self.update_detailed_forecast_label(daily_forecasts[0].period_name, daily_forecasts[0].detailed_forecast)

        # Update the generated time label
        self.daily_generated_time.setPlainText(f"Daily forecast generated at {daily_forecast_generated_time}")

    def _clear_forecast_cards(self):
        """Clears all the forecast cards currently in the scroll layout."""
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def update_detailed_forecast_label(self, period_name, detailed_forecast):
        """Updates the detailed forecast text area with the provided period name and detailed forecast."""
        text = f"{period_name}: {detailed_forecast}"
        self.detailed_forecast_label.setPlainText(text)

    def clear_data(self):
        """Clears the forecast cards, detailed forecast, and generated time."""
        self._clear_forecast_cards()
        self.detailed_forecast_label.setPlainText("")
        self.daily_generated_time.setPlainText("")


class DailyForecastCard(QFrame):
    """A widget to display daily forecast information, including weather icon, temperature, and rain chances."""

    # Signal to emit period name and detailed forecast when the "Show More" button is clicked.
    showMoreClicked = pyqtSignal(str, str)

    def __init__(self, parent=None):
        """Initializes the UI components and layout for displaying forecast details."""
        super().__init__(parent)

        # Initialize the UI components and set up the layout
        self.setStyleSheet(f"background-color: {WINDOW_BACKGROUND};")
        self.uniform_font = QFont()
        self.uniform_font.setPixelSize(24)

        # Create and configure labels with common style
        self.period_label = QLabel("", self)
        self.period_label.setFont(self.uniform_font)
        self.period_label.setAlignment(Qt.AlignCenter)
        self.period_label.setWordWrap(True)

        self.temp_label = QLabel("", self)
        self.temp_label.setFont(self.uniform_font)
        self.temp_label.setAlignment(Qt.AlignCenter)

        self.rain_label = QLabel("", self)
        self.rain_label.setFont(self.uniform_font)
        self.rain_label.setAlignment(Qt.AlignCenter)

        self.icon_label = QLabel("", self)
        self.icon_label.setFont(self.uniform_font)
        self.icon_label.setAlignment(Qt.AlignCenter)

        # Create "Show More" button and connect it to the handler
        self.show_more_button = QPushButton("Show More", self)
        self.show_more_button.setFont(self.uniform_font)
        self.show_more_button.clicked.connect(self.on_show_more_clicked)
        self.show_more_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {WIDGET_BACKGROUND};
                border: none;
                border-radius: 4px;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: {HIGHLIGHT_BACKGROUND};
            }}
        """)

        # Set up the layout
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(5, 5, 5, 5)

        # Add widgets to layout
        self.layout.addWidget(self.period_label)
        self.layout.addWidget(self.temp_label)
        self.layout.addWidget(self.rain_label)
        self.layout.addWidget(self.icon_label)
        self.layout.addWidget(self.show_more_button, alignment=Qt.AlignCenter)

        self.setLayout(self.layout)

        # Set up the network manager for fetching weather icon images
        self.manager = QNetworkAccessManager(self)
        self.manager.finished.connect(self.on_image_loaded)

        # Initialize period_name and detailed_forecast to None (to prevent crashes before it's set)
        self.period_name = None
        self.detailed_forecast = None

    def update_data(self, forecast):
        """Populate the card with forecast data and trigger the image fetch."""
        self.period_label.setText(forecast.period_name)
        self.temp_label.setText(forecast.temperature_fahrenheit)
        self.rain_label.setText(forecast.precipitation_probability)
        self.icon_label.setText(f"Icon: {forecast.weather_icon_url}")
        self.period_name = forecast.period_name
        self.detailed_forecast = forecast.detailed_forecast

        # Request the weather icon image using the URL from forecast data
        request = QNetworkRequest(QUrl(forecast.weather_icon_url))
        self.manager.get(request)

    def on_image_loaded(self, reply):
        """Handles the completion of the image fetch and sets it on the icon label."""
        if reply.error():
            self.icon_label.setText("Failed to load image")
        else:
            data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.icon_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))

        reply.deleteLater()

    def on_show_more_clicked(self):
        """Emits a signal with period name and detailed forecast when the button is clicked."""
        if self.period_name and self.detailed_forecast:
            self.showMoreClicked.emit(self.period_name, self.detailed_forecast)
