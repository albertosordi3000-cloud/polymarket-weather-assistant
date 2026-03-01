"""Lettura configurazione runtime semplice.

Mantiene default sicuri:
- data_mode = mock

Nota: parser minimale senza dipendenze esterne per massima robustezza locale.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def load_settings() -> dict[str, Any]:
    """Carica settings.yaml con parsing minimo del solo `data_mode`.

    Se il file manca o non è leggibile, ritorna default mock.
    """
    default = {"data_mode": "mock"}
    settings_path = Path(__file__).with_name("settings.yaml")

    if not settings_path.exists():
        return default

    try:
        text = settings_path.read_text(encoding="utf-8")
    except Exception:
        return default

    data_mode = "mock"
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("data_mode:"):
            value = line.split(":", 1)[1].strip().strip('"').strip("'")
            data_mode = value.lower() or "mock"
            break

    if data_mode not in {"mock", "live"}:
        data_mode = "mock"

    return {"data_mode": data_mode}


def get_data_mode() -> str:
    """Ritorna modalità dati attiva (mock default)."""
    settings = load_settings()
    mode = str(settings.get("data_mode", "mock")).strip().lower()
    return mode if mode in {"mock", "live"} else "mock"
