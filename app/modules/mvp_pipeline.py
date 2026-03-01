"""Pipeline MVP simulata end-to-end.

Flusso:
1) provider mercati (mock/live)
2) provider meteo (mock/live)
3) pricing_engine semplificato
4) signal_ranker
5) risk_filter prudenziale

Nota: live mode è solo predisposta e fa fallback a mock in questo step.
"""

from app.modules.models import RankedSignal
from app.modules.pricing_engine import estimate_fair_probability
from app.modules.risk_filter import filter_signals
from app.modules.signal_ranker import build_ranked_signal, rank_signals
from app.providers.factory import ProviderBundle, get_providers
from app.providers.mock_market_provider import MockMarketDataProvider
from app.providers.mock_weather_provider import MockWeatherDataProvider


def _safe_get_data(bundle: ProviderBundle):
    """Recupera dati dai provider; fallback a mock se live non implementato."""
    try:
        markets = bundle.market_provider.get_active_temperature_markets()
        weather_map = bundle.weather_provider.get_weather_snapshots()
        source_mode = bundle.mode
    except NotImplementedError:
        # fallback prudente per mantenere demo sempre stabile
        mock_market = MockMarketDataProvider()
        mock_weather = MockWeatherDataProvider()
        markets = mock_market.get_active_temperature_markets()
        weather_map = mock_weather.get_weather_snapshots()
        source_mode = "mock"

    return markets, weather_map, source_mode


def run_simulated_cycle() -> dict[str, object]:
    """Esegue un ciclo completo e restituisce risultati pronti per UI."""
    bundle = get_providers()
    markets, weather_map, source_mode = _safe_get_data(bundle)

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
        "mode": source_mode,
        "all": ranked,
        "valid": rank_signals(valid),
        "rejected": rank_signals(rejected),
    }
