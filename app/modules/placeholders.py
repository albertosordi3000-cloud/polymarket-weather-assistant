"""Placeholder dei moduli principali.

Questo file evita implementazioni premature:
- niente API reali
- niente pricing reale
- niente segnali reali
"""


def get_system_status() -> dict:
    """Restituisce uno stato mock dell'app.

    Serve solo per mostrare l'organizzazione del codice.
    """
    return {
        "market_feed": "mock",
        "weather_feed": "mock",
        "pricing": "not_implemented",
        "signals": "not_implemented",
    }
