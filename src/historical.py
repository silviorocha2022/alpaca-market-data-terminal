from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit

from src.config import get_settings
from src.data_connector import get_historical_client, resolve_data_feed


def get_historical_bars(
    client: StockHistoricalDataClient,
    symbol: str,
    days: int = 30,
    timeframe_value: int = 5,
    timeframe_unit: TimeFrameUnit = TimeFrameUnit.Minute,
) -> pd.DataFrame:
    end = datetime.now(UTC)
    start = end - timedelta(days=days)
    settings = get_settings()

    request = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame(timeframe_value, timeframe_unit),
        start=start,
        end=end,
        feed=resolve_data_feed(settings.data_feed),
    )

    bars = client.get_stock_bars(request)
    df = bars.df
    if df.empty:
        return df

    if isinstance(df.index, pd.MultiIndex):
        df = df.xs(symbol, level="symbol")

    return df.reset_index()


def fetch_daily_ohlcv(
    symbol: str,
    years: int = 5,
    client: StockHistoricalDataClient | None = None,
    feed_name: str | None = None,
) -> pd.DataFrame:
    """Fetch daily OHLCV bars for one ticker over the requested year window."""
    end = datetime.now(UTC)
    start = end - timedelta(days=int(years * 365.25) + 14)

    settings = get_settings()
    historical_client = client or get_historical_client(settings)
    data_feed = resolve_data_feed(feed_name or settings.data_feed)

    request = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame(1, TimeFrameUnit.Day),
        start=start,
        end=end,
        feed=data_feed,
        limit=10_000,
    )

    bars = historical_client.get_stock_bars(request)
    df = bars.df
    if df.empty:
        return df

    if isinstance(df.index, pd.MultiIndex):
        df = df.xs(symbol, level="symbol")

    result = df.reset_index()
    if "timestamp" in result.columns:
        result = result.sort_values("timestamp")
    return result.reset_index(drop=True)
