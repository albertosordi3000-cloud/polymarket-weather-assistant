"""Modelli dati semplici per il MVP simulato.

Tutto in questo file è pensato per essere leggibile e facile da estendere.
Non ci sono connessioni reali o logiche di esecuzione ordini.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


OutcomeType = Literal["YES", "NO"]


@dataclass
class Market:
    """Mercato meteo simulato in formato semplificato."""

    market_id: str
    title: str
    area: str
    threshold_c: float
    direction: Literal[">", "<"]
    implied_probability: float  # 0..1
    liquidity_usd: float
    spread_percent: float


@dataclass
class WeatherSnapshot:
    """Dati meteo simulati (attuale + forecast + qualità)."""

    area: str
    current_temp_c: float
    forecast_mean_c: float
    forecast_std_c: float
    model_divergence_c: float
    quality_score: int  # 0..100


@dataclass
class PricingResult:
    """Output base del pricing semplificato."""

    fair_probability: float  # 0..1
    confidence_score: int  # 0..100
    note: str


@dataclass
class RankedSignal:
    """Segnale dopo confronto fair vs implicita e ranking."""

    market_id: str
    market_title: str
    area: str
    suggested_outcome: OutcomeType
    price: float
    implied_probability: float
    fair_probability: float
    edge_percent: float
    confidence_score: int
    risk_score: int
    liquidity_usd: float
    spread_percent: float
    status: str
    judgement: str
    reasoning: str
