"""Factory provider per modalità mock/live.

- mock: pienamente funzionante
- live: solo predisposizione (stub) in questo step
"""

from __future__ import annotations

from app.config.runtime import get_data_mode
from app.providers.base import MarketDataProvider, WeatherDataProvider
from app.providers.live_market_provider import LiveMarketDataProvider
from app.providers.live_weather_provider import LiveWeatherDataProvider
from app.providers.mock_market_provider import MockMarketDataProvider
from app.providers.mock_weather_provider import MockWeatherDataProvider


class ProviderBundle:
    """Contenitore provider usati dalla pipeline."""

    def __init__(self, market_provider: MarketDataProvider, weather_provider: WeatherDataProvider, mode: str):
        self.market_provider = market_provider
        self.weather_provider = weather_provider
        self.mode = mode


def get_providers() -> ProviderBundle:
    """Restituisce provider in base alla modalità configurata.

    Se `live` non è pronto/abilitato correttamente, fallback automatico a mock.
    """
    mode = get_data_mode()

    if mode == "live":
        # Predisposizione futura: al momento gli adapter live sono stub.
        # Fallback prudente a mock per non rompere la demo.
        try:
            return ProviderBundle(
                market_provider=LiveMarketDataProvider(),
                weather_provider=LiveWeatherDataProvider(),
                mode="live",
            )
        except Exception:
            pass

    return ProviderBundle(
        market_provider=MockMarketDataProvider(),
        weather_provider=MockWeatherDataProvider(),
        mode="mock",
    )
