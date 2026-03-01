"""Provider mock per mercati.

Usa il modulo già esistente `market_scanner` per retrocompatibilità.
"""

from app.modules.market_scanner import scan_active_temperature_markets
from app.modules.models import Market


class MockMarketDataProvider:
    """Implementazione mock (default) per mercati temperatura."""

    def get_active_temperature_markets(self) -> list[Market]:
        return scan_active_temperature_markets()
