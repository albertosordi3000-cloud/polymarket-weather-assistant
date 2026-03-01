"""Modulo signal_ranker (MVP simulato).

Confronta probabilità implicita vs fair e produce segnali ordinabili.
"""

from app.modules.models import Market, PricingResult, RankedSignal


def _clamp_score(value: int) -> int:
    return max(0, min(100, value))


def build_ranked_signal(market: Market, pricing: PricingResult) -> RankedSignal:
    """Crea un segnale con metriche base e classificazione semplice."""
    fair_yes = pricing.fair_probability
    implied_yes = market.implied_probability

    edge_yes = (fair_yes - implied_yes) * 100
    edge_no = ((1 - fair_yes) - (1 - implied_yes)) * 100

    if edge_yes >= edge_no:
        suggested_outcome = "YES"
        selected_edge = edge_yes
    else:
        suggested_outcome = "NO"
        selected_edge = edge_no

    liquidity_penalty = 0
    if market.liquidity_usd < 15000:
        liquidity_penalty = 18
    elif market.liquidity_usd < 30000:
        liquidity_penalty = 10

    spread_penalty = 0
    if market.spread_percent > 1.0:
        spread_penalty = 20
    elif market.spread_percent > 0.8:
        spread_penalty = 8

    weak_edge_penalty = 15 if selected_edge < 4 else 0

    risk_score = _clamp_score(40 + liquidity_penalty + spread_penalty + weak_edge_penalty)

    if selected_edge >= 6 and pricing.confidence_score >= 85 and risk_score <= 45:
        judgement = "Alta qualità"
    elif selected_edge >= 4 and pricing.confidence_score >= 75 and risk_score <= 60:
        judgement = "Buona opportunità"
    elif selected_edge >= 2 and pricing.confidence_score >= 60:
        judgement = "Speculativa"
    else:
        judgement = "Da evitare"

    status = "Monitorare"
    if judgement == "Alta qualità":
        status = "Valutare ingresso manuale"
    elif judgement == "Da evitare":
        status = "Scartare"

    reasoning = (
        f"Edge {selected_edge:.2f}%, confidenza {pricing.confidence_score}/100, "
        f"rischio {risk_score}/100."
    )

    return RankedSignal(
        market_id=market.market_id,
        market_title=market.title,
        area=market.area,
        suggested_outcome=suggested_outcome,
        price=market.implied_probability,
        implied_probability=market.implied_probability,
        fair_probability=pricing.fair_probability,
        edge_percent=selected_edge,
        confidence_score=pricing.confidence_score,
        risk_score=risk_score,
        liquidity_usd=market.liquidity_usd,
        spread_percent=market.spread_percent,
        status=status,
        judgement=judgement,
        reasoning=reasoning,
    )


def rank_signals(signals: list[RankedSignal]) -> list[RankedSignal]:
    """Ordina i segnali: prima qualità, poi edge, poi rischio."""
    judgement_rank = {
        "Alta qualità": 0,
        "Buona opportunità": 1,
        "Speculativa": 2,
        "Da evitare": 3,
    }
    return sorted(
        signals,
        key=lambda s: (
            judgement_rank.get(s.judgement, 99),
            -s.edge_percent,
            -s.confidence_score,
            s.risk_score,
        ),
    )
