"""Provider live meteo (stub).

NON è attivo in questo step.
Serve solo come predisposizione per future connessioni reali in sola lettura.
"""

from app.modules.models import WeatherSnapshot


class LiveWeatherDataProvider:
    """Stub provider live per dati meteo (read-only future)."""

    def get_weather_snapshots(self) -> dict[str, WeatherSnapshot]:
        raise NotImplementedError(
            "Live weather provider non implementato in questo step. "
            "Rimane disponibile solo la modalità mock."
        )
