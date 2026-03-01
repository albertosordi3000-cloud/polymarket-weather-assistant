"""Modulo risk_filter (MVP simulato).

Applica regole prudenziali per scartare segnali rumorosi/deboli.
"""

from app.modules.models import RankedSignal


MIN_EDGE_PERCENT = 4.0
MIN_CONFIDENCE = 75
MAX_RISK_SCORE = 65
MAX_SPREAD_PERCENT = 1.2
MIN_LIQUIDITY_USD = 15000


def filter_signals(signals: list[RankedSignal]) -> tuple[list[RankedSignal], list[RankedSignal]]:
    """Separa segnali validi da segnali scartati con regole semplici.

    Returns:
        (valid_signals, rejected_signals)
    """
    valid_signals: list[RankedSignal] = []
    rejected_signals: list[RankedSignal] = []

    for signal in signals:
        if signal.edge_percent < MIN_EDGE_PERCENT:
            signal.status = "Scartato: edge insufficiente"
            signal.judgement = "Da evitare"
            rejected_signals.append(signal)
            continue
        if signal.confidence_score < MIN_CONFIDENCE:
            signal.status = "Scartato: confidenza bassa"
            signal.judgement = "Da evitare"
            rejected_signals.append(signal)
            continue
        if signal.risk_score > MAX_RISK_SCORE:
            signal.status = "Scartato: rischio elevato"
            signal.judgement = "Da evitare"
            rejected_signals.append(signal)
            continue
        if signal.spread_percent > MAX_SPREAD_PERCENT:
            signal.status = "Scartato: spread troppo alto"
            signal.judgement = "Da evitare"
            rejected_signals.append(signal)
            continue
        if signal.liquidity_usd < MIN_LIQUIDITY_USD:
            signal.status = "Scartato: liquidità troppo bassa"
            signal.judgement = "Da evitare"
            rejected_signals.append(signal)
            continue

        valid_signals.append(signal)

    return valid_signals, rejected_signals
