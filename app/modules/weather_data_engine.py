"""Modulo weather_data_engine (MVP simulato).

Responsabilità in questa fase:
- Restituire dati meteo mock (attuale + forecast).
- Includere una misura semplice di incertezza e qualità.
"""

from app.modules.models import WeatherSnapshot


def get_weather_snapshots() -> dict[str, WeatherSnapshot]:
    """Simula feed meteo professionale con valori fittizi ma plausibili."""
    snapshots = [
        WeatherSnapshot(
            area="Roma",
            current_temp_c=32.1,
            forecast_mean_c=35.8,
            forecast_std_c=1.6,
            model_divergence_c=0.8,
            quality_score=84,
        ),
        WeatherSnapshot(
            area="Madrid",
            current_temp_c=34.5,
            forecast_mean_c=37.6,
            forecast_std_c=1.2,
            model_divergence_c=0.6,
            quality_score=88,
        ),
        WeatherSnapshot(
            area="Berlino",
            current_temp_c=27.0,
            forecast_mean_c=30.3,
            forecast_std_c=2.8,
            model_divergence_c=2.2,
            quality_score=62,
        ),
        WeatherSnapshot(
            area="Parigi",
            current_temp_c=20.4,
            forecast_mean_c=17.4,
            forecast_std_c=1.1,
            model_divergence_c=0.7,
            quality_score=86,
        ),
        WeatherSnapshot(
            area="Atene",
            current_temp_c=36.9,
            forecast_mean_c=39.6,
            forecast_std_c=2.4,
            model_divergence_c=2.0,
            quality_score=64,
        ),
    ]
    return {item.area: item for item in snapshots}
