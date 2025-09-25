from PyQt5.QtWidgets import QTabWidget
from .colors import HIGHLIGHT_BACKGROUND, WIDGET_BACKGROUND, WINDOW_BACKGROUND
from .daily_forecast import DailyForecastTab
from .hourly_forecast import HourlyForecastTab


class ForecastTabsWidget(QTabWidget):
    """A tab widget containing a 'Daily Forecast' tab and an 'Hourly Forecast' tab."""

    def __init__(self, parent=None):
        """Initializes the UI components and layout for displaying the tabs."""
        super().__init__(parent)

        self.setStyleSheet(f"""
            QTabWidget::pane {{
                background: {WINDOW_BACKGROUND};
                border: none;
                padding-top: 3px;
            }}
            QTabBar::tab {{
                background: {WIDGET_BACKGROUND};
                min-width: 75px;
                padding: 5px;
            }}
            QTabBar::tab:selected {{
                background: {HIGHLIGHT_BACKGROUND};
            }}
        """)

        # Create and initialize the forecast tabs
        self.daily_tab = DailyForecastTab()
        self.hourly_tab = HourlyForecastTab()

        # Add tabs to the widget
        self.addTab(self.daily_tab, "Daily")
        self.addTab(self.hourly_tab, "Hourly")

    def update_data(self, daily_generated_time, hourly_generated_time, daily_forecasts, hourly_forecasts):
        """Updates both the Daily and Hourly forecast tabs with new forecast data."""
        self.daily_tab.update_data(daily_generated_time, daily_forecasts)
        self.hourly_tab.update_data(hourly_generated_time, hourly_forecasts)

    def clear_data(self):
        """Clears all forecast data from both tabs."""
        self.daily_tab.clear_data()
        self.hourly_tab.clear_data()
