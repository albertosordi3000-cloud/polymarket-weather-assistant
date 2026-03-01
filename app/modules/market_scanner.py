"""Modulo market_scanner (MVP simulato).

Responsabilità in questa fase:
- Restituire un piccolo set di mercati temperatura mock.
- Evitare qualsiasi connessione reale a Polymarket.
"""

from app.modules.models import Market


def scan_active_temperature_markets() -> list[Market]:
    """Simula la lettura di mercati meteo attivi.

    I valori sono artificiali ma coerenti, utili per testare la pipeline.
    """
    return [
        Market(
            market_id="mkt-rome-35",
            title="Roma: temperatura massima > 35°C domani?",
            area="Roma",
            threshold_c=35.0,
            direction=">",
            implied_probability=0.44,
            liquidity_usd=52000,
            spread_percent=0.6,
        ),
        Market(
            market_id="mkt-madrid-38",
            title="Madrid: temperatura massima > 38°C domani?",
            area="Madrid",
            threshold_c=38.0,
            direction=">",
            implied_probability=0.31,
            liquidity_usd=41000,
            spread_percent=0.8,
        ),
        Market(
            market_id="mkt-berlin-30",
            title="Berlino: temperatura massima > 30°C domani?",
            area="Berlino",
            threshold_c=30.0,
            direction=">",
            implied_probability=0.47,
            liquidity_usd=17000,
            spread_percent=1.4,
        ),
        Market(
            market_id="mkt-paris-18",
            title="Parigi: temperatura minima < 18°C stanotte?",
            area="Parigi",
            threshold_c=18.0,
            direction="<",
            implied_probability=0.52,
            liquidity_usd=28000,
            spread_percent=0.9,
        ),
        Market(
            market_id="mkt-athens-40",
            title="Atene: temperatura massima > 40°C domani?",
            area="Atene",
            threshold_c=40.0,
            direction=">",
            implied_probability=0.22,
            liquidity_usd=12000,
            spread_percent=1.9,
        ),
    ]
