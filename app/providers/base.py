"""Interfacce provider (sola lettura) per modalità mock/live.

Scopo:
- separare la logica di business dal modo in cui arrivano i dati.
- mantenere mock mode stabile come default.
- preparare future integrazioni live senza rompere la demo.
"""

from __future__ import annotations

from typing import Protocol

from app.modules.models import Market, WeatherSnapshot


class MarketDataProvider(Protocol):
    """Interfaccia per lettura mercati (no trading, sola lettura)."""

    def get_active_temperature_markets(self) -> list[Market]:
        """Restituisce mercati temperatura disponibili per analisi."""


class WeatherDataProvider(Protocol):
    """Interfaccia per lettura dati meteo (sola lettura)."""

    def get_weather_snapshots(self) -> dict[str, WeatherSnapshot]:
        """Restituisce snapshot meteo per area."""
