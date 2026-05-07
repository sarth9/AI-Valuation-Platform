import yfinance as yf


def fetch_company_market_data(ticker: str) -> dict:
    """
    Fetch real company market data from Yahoo Finance.
    """
    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "ticker": ticker.upper(),
        "company_name": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "actual_market_cap": info.get("marketCap"),
        "enterprise_value": info.get("enterpriseValue"),
        "total_revenue": info.get("totalRevenue"),
        "ebitda": info.get("ebitda"),
        "net_income": info.get("netIncomeToCommon"),
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
    }