"""Provider mock per meteo.

Usa il modulo già esistente `weather_data_engine` per retrocompatibilità.
"""

from app.modules.models import WeatherSnapshot
from app.modules.weather_data_engine import get_weather_snapshots


class MockWeatherDataProvider:
    """Implementazione mock (default) per dati meteo."""

    def get_weather_snapshots(self) -> dict[str, WeatherSnapshot]:
        return get_weather_snapshots()
