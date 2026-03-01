"""Pipeline MVP simulata end-to-end.

Flusso:
1) market_scanner mock
2) weather_data_engine mock
3) pricing_engine semplificato
4) signal_ranker
5) risk_filter prudenziale
"""

from app.modules.market_scanner import scan_active_temperature_markets
from app.modules.models import RankedSignal
from app.modules.pricing_engine import estimate_fair_probability
from app.modules.risk_filter import filter_signals
from app.modules.signal_ranker import build_ranked_signal, rank_signals
from app.modules.weather_data_engine import get_weather_snapshots


def run_simulated_cycle() -> dict[str, list[RankedSignal]]:
    """Esegue un ciclo simulato completo e restituisce risultati pronti per UI."""
    markets = scan_active_temperature_markets()
    weather_map = get_weather_snapshots()

    raw_signals: list[RankedSignal] = []
    for market in markets:
        weather = weather_map.get(market.area)
        if weather is None:
            continue
        pricing = estimate_fair_probability(market, weather)
        signal = build_ranked_signal(market, pricing)
        raw_signals.append(signal)

    ranked = rank_signals(raw_signals)
    valid, rejected = filter_signals(ranked)

    return {
        "all": ranked,
        "valid": rank_signals(valid),
        "rejected": rank_signals(rejected),
    }
