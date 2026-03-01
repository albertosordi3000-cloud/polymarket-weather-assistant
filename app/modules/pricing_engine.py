"""Modulo pricing_engine (MVP simulato).

Obiettivo: stimare una probabilità fair semplice e prudente a partire dal meteo mock.
Formula volutamente basilare per mantenere il sistema leggibile.
"""

from __future__ import annotations

import math

from app.modules.models import Market, PricingResult, WeatherSnapshot


def _normal_cdf(x: float, mean: float, std: float) -> float:
    """CDF normale con math.erf per evitare dipendenze extra."""
    std_safe = max(std, 0.3)
    z = (x - mean) / (std_safe * math.sqrt(2.0))
    return 0.5 * (1.0 + math.erf(z))


def estimate_fair_probability(market: Market, weather: WeatherSnapshot) -> PricingResult:
    """Calcola probabilità fair con correzione prudenziale di confidenza.

    Step semplificati:
    1) Calcolo probabilità evento via distribuzione normale.
    2) Penalizzo leggermente la probabilità verso 50% in caso di incertezza.
    3) Costruisco confidence score in base a qualità dato e stabilità forecast.
    """
    if market.direction == ">":
        event_prob = 1.0 - _normal_cdf(market.threshold_c, weather.forecast_mean_c, weather.forecast_std_c)
    else:
        event_prob = _normal_cdf(market.threshold_c, weather.forecast_mean_c, weather.forecast_std_c)

    # Incertezza semplice: più alta la divergenza e la varianza, più bassa la fiducia.
    uncertainty = min(1.0, (weather.model_divergence_c / 3.0) + (weather.forecast_std_c / 6.0))

    # Prudenza: ritiro parziale verso 0.5 quando il dato è incerto.
    pull_to_center = 0.2 * uncertainty
    fair_prob = event_prob * (1.0 - pull_to_center) + 0.5 * pull_to_center

    confidence = int(
        max(
            30,
            min(
                95,
                weather.quality_score - int(25 * uncertainty),
            ),
        )
    )

    note = "Stima prudente su dati meteo mock"
    return PricingResult(fair_probability=fair_prob, confidence_score=confidence, note=note)
