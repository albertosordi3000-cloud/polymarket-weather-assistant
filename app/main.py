"""Dashboard Streamlit - MVP simulato end-to-end.

Nota importante:
- Solo dati mock della pipeline interna.
- Nessuna API reale (Polymarket/meteo).
- Nessun auto-trading o esecuzione ordini.
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime

import pandas as pd
import streamlit as st

from app.modules.mvp_pipeline import run_simulated_cycle


DISPLAY_COLUMNS = [
    "market_title",
    "area",
    "suggested_outcome",
    "implied_probability_pct",
    "fair_probability_pct",
    "edge_percent",
    "confidence_score",
    "risk_score",
    "judgement",
    "action_suggested",
    "status",
    "reasoning",
]


def _action_from_signal(status: str, judgement: str) -> str:
    """Converte stato/giudizio tecnico in azione semplice per utente non tecnico."""
    if judgement == "Alta qualità":
        return "entrare ora"
    if judgement == "Buona opportunità":
        return "attendere"
    if judgement == "Speculativa":
        return "monitorare"
    return "evitare"


def _to_dataframe(signals: list) -> pd.DataFrame:
    """Trasforma segnali dataclass in DataFrame leggibile per dashboard."""
    if not signals:
        return pd.DataFrame(columns=DISPLAY_COLUMNS)

    rows = []
    for signal in signals:
        row = asdict(signal)
        row["implied_probability_pct"] = round(row["implied_probability"] * 100, 2)
        row["fair_probability_pct"] = round(row["fair_probability"] * 100, 2)
        row["edge_percent"] = round(row["edge_percent"], 2)
        row["action_suggested"] = _action_from_signal(row["status"], row["judgement"])
        rows.append(row)

    df = pd.DataFrame(rows)
    return df


def _format_display(df: pd.DataFrame) -> pd.DataFrame:
    """Seleziona e rinomina colonne per una lettura più pulita."""
    if df.empty:
        return df

    display_df = df[DISPLAY_COLUMNS].copy()
    return display_df.rename(
        columns={
            "market_title": "Mercato",
            "area": "Area",
            "suggested_outcome": "Outcome suggerito",
            "implied_probability_pct": "Prob. implicita (%)",
            "fair_probability_pct": "Prob. fair (%)",
            "edge_percent": "Edge (%)",
            "confidence_score": "Confidence",
            "risk_score": "Risk",
            "judgement": "Giudizio finale",
            "action_suggested": "Azione suggerita",
            "status": "Stato",
            "reasoning": "Motivazione",
        }
    )


def _explain_market(signal_row: pd.Series) -> str:
    """Spiegazione sintetica del significato mercato per utente non tecnico."""
    outcome = signal_row["suggested_outcome"]
    if outcome == "YES":
        return "Il sistema vede più valore nel lato YES rispetto al prezzo attuale."
    return "Il sistema vede più valore nel lato NO rispetto al prezzo attuale."


st.set_page_config(page_title="Polymarket Weather Assistant", page_icon="🌦️", layout="wide")

st.title("🌦️ Polymarket Weather Assistant")
st.caption("Dashboard MVP simulata - supporto decisionale manuale")

st.warning(
    "Solo dati mock. Nessuna connessione reale a Polymarket o API meteo. "
    "Nessun auto-trading: il tool suggerisce, non esegue ordini."
)

# Esecuzione ciclo mock end-to-end (pipeline esistente)
results = run_simulated_cycle()
all_signals_df = _to_dataframe(results["all"])
valid_signals_df = _to_dataframe(results["valid"])
rejected_signals_df = _to_dataframe(results["rejected"])

# Watchlist: mercati monitorabili ma non già in opportunità valide e non scartati
valid_ids = set(valid_signals_df["market_id"].tolist()) if not valid_signals_df.empty else set()
rejected_ids = set(rejected_signals_df["market_id"].tolist()) if not rejected_signals_df.empty else set()
watchlist_df = all_signals_df[
    ~all_signals_df["market_id"].isin(valid_ids.union(rejected_ids))
].copy()
watchlist_df = watchlist_df.head(10)

# Filtri base
st.sidebar.header("Filtri base")
all_areas = sorted(all_signals_df["area"].unique().tolist()) if not all_signals_df.empty else []
selected_areas = st.sidebar.multiselect("Area", options=all_areas, default=all_areas)
min_edge = st.sidebar.slider("Edge minimo (%)", min_value=0.0, max_value=20.0, value=0.0, step=0.5)
min_confidence = st.sidebar.slider("Confidenza minima", min_value=0, max_value=100, value=0, step=1)
max_risk = st.sidebar.slider("Rischio massimo", min_value=0, max_value=100, value=100, step=1)


def _apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    filtered = df[df["area"].isin(selected_areas)] if selected_areas else df.iloc[0:0]
    filtered = filtered[filtered["edge_percent"] >= min_edge]
    filtered = filtered[filtered["confidence_score"] >= min_confidence]
    filtered = filtered[filtered["risk_score"] <= max_risk]
    return filtered


all_filtered = _apply_filters(all_signals_df)
valid_filtered = _apply_filters(valid_signals_df)
watchlist_filtered = _apply_filters(watchlist_df)
rejected_filtered = _apply_filters(rejected_signals_df)

# Riepilogo generale
st.header("Riepilogo generale")
last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Stato sistema", "Simulato operativo")
col2.metric("Ultimo aggiornamento", last_update)
col3.metric("Mercati analizzati", len(all_filtered))
col4.metric("Opportunità valide", len(valid_filtered))
col5.metric("Segnali scartati", len(rejected_filtered))

if valid_filtered.empty:
    st.info("Nessuna opportunità valida al momento con i filtri attuali. Meglio attendere.")

# Top opportunità
st.header("Top opportunità")
top_opportunities = valid_filtered.head(3)
if top_opportunities.empty:
    st.write("Nessuna opportunità robusta da mostrare ora.")
else:
    st.dataframe(_format_display(top_opportunities), use_container_width=True)

# Watchlist
st.header("Watchlist")
st.caption("Top 10 mercati da monitorare (separati dalle opportunità già valide)")
if watchlist_filtered.empty:
    st.write("Nessun mercato in watchlist con i filtri attuali.")
else:
    st.dataframe(_format_display(watchlist_filtered.head(10)), use_container_width=True)

# Mercati da evitare
st.header("Mercati da evitare")
if rejected_filtered.empty:
    st.write("Nessun mercato escluso dai filtri nel set corrente.")
else:
    avoid_view = _format_display(rejected_filtered)
    st.dataframe(avoid_view, use_container_width=True)

# Tabella completa
st.header("Tabella completa")
if all_filtered.empty:
    st.write("Nessun mercato disponibile con i filtri selezionati.")
else:
    st.dataframe(_format_display(all_filtered), use_container_width=True)

# Dettaglio selezione
st.header("Dettaglio selezione")
if all_filtered.empty:
    st.write("Seleziona filtri meno restrittivi per vedere un mercato nel dettaglio.")
else:
    market_options = all_filtered["market_title"].tolist()
    selected_market_title = st.selectbox("Seleziona un mercato", options=market_options)
    selected_row = all_filtered[all_filtered["market_title"] == selected_market_title].iloc[0]

    st.markdown(f"**Testo mercato:** {selected_row['market_title']}")
    st.markdown(f"**Significato sintetico:** {_explain_market(selected_row)}")
    st.markdown(
        f"**Fair vs implicita:** {selected_row['fair_probability_pct']:.2f}% vs "
        f"{selected_row['implied_probability_pct']:.2f}%"
    )
    st.markdown(f"**Motivazione del segnale:** {selected_row['reasoning']}")
    st.markdown(
        f"**Rischi principali:** rischio {selected_row['risk_score']}/100, "
        f"spread {selected_row['spread_percent']:.2f}%"
    )
    st.markdown(f"**Suggerimento finale:** {selected_row['action_suggested']}")
