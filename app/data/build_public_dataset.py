import os
import time
import pandas as pd
import yfinance as yf

from app.data.tickers import ALL_PUBLIC_TICKERS


OUTPUT_DIR = "data/public"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "raw_company_data.csv")

FEATURE_KEYS = [
    "longName",
    "sector",
    "industry",
    "marketCap",
    "enterpriseValue",
    "totalRevenue",
    "ebitda",
    "netIncomeToCommon",
    "totalCash",
    "totalDebt",
    "bookValue",
    "currentRatio",
    "debtToEquity",
    "returnOnAssets",
    "returnOnEquity",
    "grossMargins",
    "operatingMargins",
    "profitMargins",
    "revenueGrowth",
    "earningsGrowth",
    "trailingPE",
    "forwardPE",
    "priceToBook",
    "beta",
    "sharesOutstanding",
]

COLUMN_MAPPING = {
    "longName": "company_name",
    "sector": "sector",
    "industry": "industry",
    "marketCap": "market_cap",
    "enterpriseValue": "enterprise_value",
    "totalRevenue": "total_revenue",
    "ebitda": "ebitda",
    "netIncomeToCommon": "net_income",
    "totalCash": "total_cash",
    "totalDebt": "total_debt",
    "bookValue": "book_value",
    "currentRatio": "current_ratio",
    "debtToEquity": "debt_to_equity",
    "returnOnAssets": "return_on_assets",
    "returnOnEquity": "return_on_equity",
    "grossMargins": "gross_margins",
    "operatingMargins": "operating_margins",
    "profitMargins": "profit_margins",
    "revenueGrowth": "revenue_growth",
    "earningsGrowth": "earnings_growth",
    "trailingPE": "trailing_pe",
    "forwardPE": "forward_pe",
    "priceToBook": "price_to_book",
    "beta": "beta",
    "sharesOutstanding": "shares_outstanding",
}


def fetch_company_info(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    info = stock.info

    row = {"ticker": ticker}
    for key in FEATURE_KEYS:
        row[COLUMN_MAPPING[key]] = info.get(key)

    return row


def is_valid_row(row: dict) -> bool:
    if row.get("market_cap") in [None, 0]:
        return False
    if row.get("total_revenue") in [None, 0]:
        return False
    if row.get("shares_outstanding") in [None, 0]:
        return False
    return True


def build_dataset(tickers: list[str], output_path: str = OUTPUT_FILE) -> pd.DataFrame:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    rows = []
    skipped = []

    for idx, ticker in enumerate(tickers, start=1):
        try:
            print(f"[{idx}/{len(tickers)}] Fetching data for {ticker}...")
            row = fetch_company_info(ticker)

            if is_valid_row(row):
                rows.append(row)
            else:
                print(f"Skipped {ticker} due to missing critical fields.")
                skipped.append(ticker)

            time.sleep(0.8)
        except Exception as exc:
            print(f"Failed for {ticker}: {exc}")
            skipped.append(ticker)

    df = pd.DataFrame(rows)

    if not df.empty:
        df = df.drop_duplicates(subset=["ticker"]).reset_index(drop=True)

    df.to_csv(output_path, index=False)

    print("\nDataset build complete.")
    print(f"Saved raw public data to: {output_path}")
    print(f"Valid dataset shape: {df.shape}")
    print(f"Skipped count: {len(skipped)}")
    if skipped:
        print(skipped)

    print("\nMissing values per column:")
    print(df.isnull().sum())

    return df


if __name__ == "__main__":
    build_dataset(ALL_PUBLIC_TICKERS)