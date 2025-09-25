from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel


class ForecastHeadingWidget(QLabel):
    """Widget displaying the forecast heading with location."""

    def __init__(self, parent=None):
        """Initializes UI components."""
        super().__init__(parent)

        self.setText("Forecast for...")
        self.setWordWrap(True)

        font = QFont()
        font.setPixelSize(27)
        self.setFont(font)

    def update_data(self, address):
        """Updates the heading with the given address."""
        self.setText(f"Forecast for {address}")

    def clear_data(self):
        self.setText("Forecast for...")
