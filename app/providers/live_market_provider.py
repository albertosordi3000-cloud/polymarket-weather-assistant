"""Provider live mercati (stub).

NON è attivo in questo step.
Serve solo come predisposizione per future connessioni reali in sola lettura.
"""

from app.modules.models import Market


class LiveMarketDataProvider:
    """Stub provider live per mercati Polymarket (read-only future)."""

    def get_active_temperature_markets(self) -> list[Market]:
        raise NotImplementedError(
            "Live market provider non implementato in questo step. "
            "Rimane disponibile solo la modalità mock."
        )
