# alpaca-market-data-terminal

Mini market data terminal using Alpaca APIs for historical OHLCV charts and live bid/ask quote updates in a simple Python-based UI.

## Project Goal

This project is to build a terminal that connects to Alpaca market data, retrieves historical OHLCV bars, displays a chart, and provides a simple UI for real-time quotes for US-listed stocks and ETFs.

## Setup

Create and activate the conda environment:

```bash
conda env create -f environment.yml
conda activate alpaca-terminal
```

Create a local `.env` file from the example:

```bash
cp .env.example .env
```

Then add your Alpaca paper-trading API key and secret to `.env`.

## Run

```bash
streamlit run app.py
```

## Repository Structure

```text
alpaca-market-data-terminal/
├── app.py                  # Streamlit app entrypoint and UI layout
├── src/
│   ├── __init__.py
│   ├── config.py           # Loads Alpaca credentials and app settings from environment variables
│   ├── data_connector.py   # Builds Alpaca market data clients and resolves data feed settings
│   ├── historical.py       # Fetches historical OHLCV bar data
│   ├── live_quotes.py      # Fetches latest bid, ask, last trade, and quote timestamps
│   ├── company.py          # Resolves ticker symbols to company names
│   └── company_search.py   # Provides equity dropdown choices and fuzzy company/ticker search logic
├── screenshots/
│   └── .gitkeep            # Placeholder for optional UI screenshots
├── .env.example            # Template for required Alpaca API credentials
├── .gitignore              # Excludes local secrets, caches, and system files
├── environment.yml         # Conda environment specification
├── requirements.txt        # Python package requirements
├── LICENSE                 # Project license
├── SKILL.md                # Project-specific workflow notes
└── README.md               # Project overview, setup, and usage instructions
```

## Security Notes

DO NOT commit `.env` or real API credentials. Commit `.env.example` only.
