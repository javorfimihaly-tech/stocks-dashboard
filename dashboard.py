import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import pandas_market_calendars as mcal

st.title("Részvényfigyelő Dashboard – Automatikus frissítéssel")

# A részvények listája
TICKERS = ["WAF", "FMV", "NANO", "BYW6", "BC8", "SMCP", "DHER"]

# --- 1. Előző kereskedési nap ---
nyse = mcal.get_calendar("NYSE")
schedule = nyse.schedule(start_date=datetime.now() - timedelta(days=7),
                         end_date=datetime.now())
last_trading_day = schedule.index[-1].strftime("%Y-%m-%d")

st.write(f"Legutóbbi kereskedési nap: **{last_trading_day}**")

# --- 2. Adatok lekérése ---
rows = []
for t in TICKERS:
    try:
        hist = yf.Ticker(t).history(start=last_trading_day,
                                    end=datetime.now().strftime("%Y-%m-%d"))
        row = hist.iloc[-1]
        rows.append({
            "Ticker": t,
            "Open": row["Open"],
            "High": row["High"],
            "Low": row["Low"],
            "Close": row["Close"],
            "Volume": row["Volume"]
        })
    except:
        rows.append({
            "Ticker": t,
            "Open": None,
            "High": None,
            "Low": None,
            "Close": None,
            "Volume": None
        })

df = pd.DataFrame(rows)
st.dataframe(df)

# Chart
st.subheader("Záróárak")
st.line_chart(df.set_index("Ticker")["Close"])
