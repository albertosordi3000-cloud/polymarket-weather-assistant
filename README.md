# Polymarket Weather Assistant (MVP Simulato)

Questa repo contiene una **demo Streamlit simulata** (senza API reali) per supporto decisionale manuale sui mercati meteo.

## Stato attuale del progetto
La demo oggi:
- usa solo dati mock/simulati;
- mostra dashboard, ranking, watchlist e segnali scartati;
- **non** esegue trade;
- **non** si collega a Polymarket reale;
- **non** usa API meteo reali.

## Requisiti minimi (Windows)
- Windows 10 o 11
- Python **3.10+** (consigliato 3.11)
- Connessione internet (solo per installare dipendenze la prima volta)

---

## Guida semplice per avvio locale su Windows (principiante assoluto)

## 1) Installa Python (se non lo hai)
1. Vai su: https://www.python.org/downloads/
2. Scarica Python 3.11 (o versione recente compatibile)
3. Durante l'installazione, **spunta** la casella: `Add Python to PATH`
4. Completa l'installazione

Per verificare che Python sia installato:
- apri **Prompt dei comandi**
- scrivi:
  - `python --version`

Se compare una versione (es. `Python 3.11.x`), è ok.

## 2) Apri la cartella del progetto
Puoi usare due modi:

### Metodo A (più semplice)
- Apri Esplora File
- Vai nella cartella del progetto
- Clicca sulla barra percorso, scrivi `cmd`, premi Invio

### Metodo B
- Apri Prompt dei comandi
- Usa `cd` fino alla cartella progetto (esempio sotto nei comandi finali)

## 3) (Consigliato) Crea ambiente virtuale
Questo serve a non sporcare Python globale:

- crea ambiente:
  - `python -m venv .venv`
- attiva ambiente:
  - `\.venv\Scripts\activate`

Quando è attivo, vedrai `(.venv)` a sinistra nel terminale.

## 4) Installa le dipendenze
Con ambiente attivo:
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`

## 5) Avvia la web app
- `streamlit run app/main.py`

## 6) Cosa aspettarti quando funziona
- Si apre una pagina web (o vedi un link nel terminale)
- In genere l'indirizzo è: `http://localhost:8501`
- Vedrai la dashboard con:
  - riepilogo generale,
  - top opportunità mock,
  - watchlist,
  - mercati da evitare,
  - dettaglio mercato selezionato.

---

## Errori comuni e soluzione rapida

## Errore: `python non è riconosciuto`
- Python non è installato o non è nel PATH.
- Reinstalla Python e spunta `Add Python to PATH`.

## Errore: `pip non è riconosciuto`
- Usa: `python -m pip install -r requirements.txt`

## Errore: `streamlit non è riconosciuto`
- Ambiente virtuale non attivo, oppure dipendenze non installate.
- Esegui:
  - `\.venv\Scripts\activate`
  - `pip install -r requirements.txt`

## Errore su porta già in uso (8501)
- Chiudi eventuale altra app Streamlit aperta
- oppure avvia su altra porta:
  - `streamlit run app/main.py --server.port 8502`

## Errore durante installazione pacchetti
- Verifica connessione internet
- Aggiorna pip:
  - `python -m pip install --upgrade pip`
- Riprova `pip install -r requirements.txt`

---

## Dipendenze minime usate
- `streamlit` (interfaccia web)
- `pandas` (tabelle dashboard)
- `pyyaml` (configurazioni YAML)

---

## Comandi da copiare e incollare
> Esegui questi comandi nel Prompt dei comandi, uno per riga, nell'ordine.

```bat
cd C:\percorso\alla\cartella\polymarket-weather-assistant
python --version
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app/main.py
```

Se vuoi avviare su porta diversa:

```bat
streamlit run app/main.py --server.port 8502
```
