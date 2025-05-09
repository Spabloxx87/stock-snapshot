# Install required packages
!pip install yfinance pandas --quiet

import yfinance as yf
import pandas as pd
from datetime import datetime
from google.colab import files

# Define portfolio (38 tickers, JE00B78CGV99.SG removed)
portfolio = [
    {"Name": "Pfiser", "Code": "PFE"},
    {"Name": "Alphabet", "Code": "GOOGL"},
    {"Name": "Nike", "Code": "NKE"},
    {"Name": "Blackrock", "Code": "BLK"},
    {"Name": "DJI", "Code": "^DJI"},
    {"Name": "S&P 500", "Code": "^GSPC"},
    {"Name": "VIX", "Code": "^VIX"},
    {"Name": "ASML", "Code": "ASML.AS"},
    {"Name": "iShares Core MSCI Europe UCITS ETF EUR (Acc)", "Code": "IMAE.AS"},
    {"Name": "GOAI.MI", "Code": "GOAI.MI"},
    {"Name": "iShares $ Treasury Bd 7-10y UCITS ETF USD Dis", "Code": "IDTM.L"},
    {"Name": "iShares MSCI Global Semiconductors UCITS ETF USD Acc", "Code": "SEME.MI"},
    {"Name": "iShares MSCI USA Qlty Dividend UCITS ETF USD Dis", "Code": "QDVD.DE"},
    {"Name": "ISHSII-J.P.M.$ EM BOND U.ETF", "Code": "IUS7.DE"},
    {"Name": "SPDR S&P Euro Dividend Aristocrats ETF", "Code": "EUDV.MI"},
    {"Name": "SPDR S&P US DIV ARISTOCRATS UCITS ETF", "Code": "USDV.MI"},
    {"Name": "WisdomTree Physical Gold", "Code": "PHAU.MI"},
    {"Name": "ADR Taiwan Semiconductor Manufacturing", "Code": "TSM"},
    {"Name": "Roche", "Code": "ROG.SW"},
    {"Name": "Royalty Pharma", "Code": "RPRX"},
    {"Name": "Medtronic", "Code": "2M6.F"},
    {"Name": "Vanguard S&P 500 UCITS ETF USD", "Code": "VUSA.AS"},
    {"Name": "Xtrackers Artificial Intelligence & Big Data UCITS ETF 1C", "Code": "XAIX.DE"},
    {"Name": "Amundi MSCI Robotics & AI ESG Screened UCITS ETF Acc", "Code": "GOAI.PA"},
    {"Name": "Amundi MSCI Switzerland UCITS ETF - EUR (C)", "Code": "CSW.PA"},
    {"Name": "Vanguard FTSE All-World UCITS ETF USD Dis", "Code": "VWRL.AS"},
    {"Name": "iShares Govt Bond 7-10yr UCITS ETF EUR", "Code": "IBGM.AS"},
    {"Name": "iShares Core MSCI World UCITS ETF USD (Acc)", "Code": "IWDA.AS"},
    {"Name": "VanEck World Equal Weight Screened UCITS ETF", "Code": "TSWE.MI"},
    {"Name": "USD/CHF", "Code": "USDCHF=X"},
    {"Name": "EUR/CHF", "Code": "EURCHF=X"},
    {"Name": "EUR/USD", "Code": "EURUSD=X"},
    {"Name": "CHF/USD", "Code": "CHFUSD=X"},
    {"Name": "CHF/EUR", "Code": "CHFEUR=X"},
    {"Name": "USD/EUR", "Code": "USDEUR=X"},
    {"Name": "Nasdaq", "Code": "^NDX"},
    {"Name": "iShares NASDAQ 100 UCITS ETF USD (Acc)", "Code": "CNDX.AS"}
]

# Collect data
data_rows = []

for item in portfolio:
    name = item["Name"]
    symbol = item["Code"]
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="250d")

        if hist.empty:
            print(f"❌ No data for {name} ({symbol})")
            continue

        close = hist["Close"].dropna()
        current_price = close.iloc[-1]
        previous_close = close.iloc[-2] if len(close) > 1 else None
        ma50 = close.rolling(50).mean().iloc[-1] if len(close) >= 50 else None
        ma150 = close.rolling(150).mean().iloc[-1] if len(close) >= 150 else None
        ma200 = close.rolling(200).mean().iloc[-1] if len(close) >= 200 else None
        timestamp = datetime.now()

        data_rows.append({
            "Name": name,
            "Symbol": symbol,
            "CurrentPrice": current_price,
            "PreviousClose": previous_close,
            "MA50": ma50,
            "MA150": ma150,
            "MA200": ma200,
            "Timestamp": timestamp
        })

        print(f"✅ {symbol}: {current_price:.2f}")

    except Exception as e:
        print(f"⚠️ Error with {name} ({symbol}): {e}")

# Create and download CSV
df = pd.DataFrame(data_rows)
csv_filename = "stock_snapshot.csv"
df.to_csv(csv_filename, index=False)

print(f"\n📁 CSV ready. Attempting automatic download...")
files.download(csv_filename)
