import time
import yfinance as yf


CACHE_TTL_SECONDS = 1800  # 30 minutes
_company_cache: dict[str, dict] = {}


def _get_cached(ticker: str):
    cached = _company_cache.get(ticker)
    if not cached:
        return None

    age = time.time() - cached["timestamp"]
    if age > CACHE_TTL_SECONDS:
        _company_cache.pop(ticker, None)
        return None

    return cached["data"]


def _set_cache(ticker: str, data: dict):
    _company_cache[ticker] = {
        "timestamp": time.time(),
        "data": data,
    }


def fetch_company_market_data(ticker: str) -> dict:
    """
    Fetch real company market data from Yahoo Finance with simple in-memory caching.
    """
    ticker = ticker.upper().strip()

    cached_data = _get_cached(ticker)
    if cached_data is not None:
        return cached_data

    stock = yf.Ticker(ticker)
    info = stock.info

    if not info:
        raise ValueError("No company data returned from Yahoo Finance.")

    data = {
        "ticker": ticker,
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

    _set_cache(ticker, data)
    return data
