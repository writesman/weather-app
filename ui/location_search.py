import os
from services import GeolocatorService
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from .colors import HIGHLIGHT_BACKGROUND, WIDGET_BACKGROUND


class LocationSearchWidget(QWidget):
    locationConfirmed = pyqtSignal(object)

    def __init__(self, parent=None):
        """Set up the UI components."""
        super().__init__(parent)
        self.geo_service = GeolocatorService()

        self.setStyleSheet(f"background-color: {WIDGET_BACKGROUND}; border: none;")

        # Configure Font
        font = QFont()
        font.setPixelSize(16)

        # Create and Configure Search Bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Enter location")
        self.search_bar.setFont(font)
        self.search_bar.setFixedHeight(40)
        self.search_bar.setStyleSheet("padding-left: 5px; padding-right: 5px")
        self.search_bar.returnPressed.connect(self.search_location)

        # Create and Configure Search Button
        self.search_button = QPushButton("Search", self)
        self.search_button.setFont(font)
        self.search_button.setFixedSize(80, 40)
        self.search_button.clicked.connect(self.search_location)
        self.search_button.setStyleSheet(f"""
            QPushButton:hover {{
                background-color: {HIGHLIGHT_BACKGROUND};
            }}
        """)

        # Layout Setup
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.search_bar)
        layout.addWidget(self.search_button)

        self.setLayout(layout)

    def search_location(self):
        """Handles location search and emits a signal if confirmed."""
        location_text = self.search_bar.text().strip()
        if not location_text:
            QMessageBox.warning(self, "Input Error", "Please enter a location.")
            return

        location = self.geo_service.get_location(location_text)
        if location:
            if self._confirm_location(location.address):
                self._clear_previous_forecast()
                self.locationConfirmed.emit(location)
                self.search_bar.clear()
        else:
            QMessageBox.warning(self, "Location Not Found",
                                "Could not find the location. Please try a different query.")

    def _geocode_location(self, location_text):
        """Fetch location data using geopy."""
        try:
            return self.geolocator.geocode(location_text)
        except Exception as e:
            QMessageBox.critical(self, "Geocoder Error", f"Error accessing geocoding service: {e}")
            return None

    def _confirm_location(self, address):
        """Prompt the user to confirm the found location."""
        return QMessageBox.question(self, "Confirm Location", f"Is this the correct location?\n\n{address}",
                                    QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes

    def _clear_previous_forecast(self):
        """Remove old forecast data files if they exist."""
        for filename in ['data/daily_forecast_data.csv', 'data/hourly_forecast_data.csv']:
            try:
                if os.path.exists(filename):
                    os.remove(filename)
            except OSError:
                pass
