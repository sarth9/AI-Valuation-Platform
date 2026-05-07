import yfinance as yf
import pandas as pd


def fetch_company_snapshot(ticker: str) -> dict:
    """
    Fetch a basic financial snapshot for a company using Yahoo Finance.
    """
    stock = yf.Ticker(ticker)
    info = stock.info

    data = {
        "ticker": ticker.upper(),
        "company_name": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "market_cap": info.get("marketCap"),
        "enterprise_value": info.get("enterpriseValue"),
        "total_revenue": info.get("totalRevenue"),
        "ebitda": info.get("ebitda"),
        "net_income_to_common": info.get("netIncomeToCommon"),
        "total_cash": info.get("totalCash"),
        "total_debt": info.get("totalDebt"),
        "book_value": info.get("bookValue"),
        "current_ratio": info.get("currentRatio"),
        "debt_to_equity": info.get("debtToEquity"),
        "return_on_assets": info.get("returnOnAssets"),
        "return_on_equity": info.get("returnOnEquity"),
        "gross_margins": info.get("grossMargins"),
        "operating_margins": info.get("operatingMargins"),
        "profit_margins": info.get("profitMargins"),
        "revenue_growth": info.get("revenueGrowth"),
        "earnings_growth": info.get("earningsGrowth"),
        "trailing_pe": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "price_to_book": info.get("priceToBook"),
        "beta": info.get("beta"),
        "shares_outstanding": info.get("sharesOutstanding"),
        "website": info.get("website"),
    }

    return data


def save_snapshot_to_csv(ticker: str, output_path: str = "data/company_snapshot.csv") -> None:
    """
    Fetch snapshot and save to CSV.
    """
    snapshot = fetch_company_snapshot(ticker)
    df = pd.DataFrame([snapshot])
    df.to_csv(output_path, index=False)
    print(f"Saved data for {ticker.upper()} to {output_path}")
    print(df.T)


if __name__ == "__main__":
    ticker = input("Enter company ticker (example: AAPL, MSFT, GOOGL): ").strip().upper()
    save_snapshot_to_csv(ticker)