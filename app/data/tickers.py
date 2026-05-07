TECH_TICKERS = [
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "META", "NVDA", "TSLA", "NFLX", "ADBE",
    "INTC", "AMD", "ORCL", "CRM", "CSCO", "IBM", "QCOM", "UBER", "PYPL", "SHOP",
    "SNOW", "PLTR", "ZM", "DOCU", "SAP", "SONY", "ASML", "AVGO", "TXN", "MU",
    "NOW", "TEAM", "PANW", "CRWD", "DDOG", "MDB", "NET", "OKTA", "INTU"
]

FINANCE_TICKERS = [
    "JPM", "BAC", "WFC", "C", "GS", "MS", "BLK", "SCHW", "AXP", "SPGI",
    "ICE", "CB", "PGR", "AIG", "MET", "TRV", "USB", "BK", "TFC", "COF"
]

HEALTHCARE_TICKERS = [
    "JNJ", "PFE", "MRK", "ABBV", "LLY", "UNH", "TMO", "DHR", "MDT", "BMY",
    "AMGN", "GILD", "CVS", "CI", "SYK", "ISRG", "VRTX", "REGN", "ZTS", "HUM"
]

ENERGY_TICKERS = [
    "XOM", "CVX", "COP", "SLB", "EOG", "MPC", "PSX", "VLO", "OXY", "KMI",
    "WMB", "BKR", "HAL", "DVN", "FANG"
]

CONSUMER_TICKERS = [
    "WMT", "COST", "PG", "KO", "PEP", "MCD", "SBUX", "NKE", "TGT", "HD",
    "LOW", "DIS", "CMCSA", "BKNG", "ABNB", "GM", "F", "EL", "CL"
]

INDUSTRIAL_TICKERS = [
    "BA", "CAT", "DE", "GE", "HON", "UPS", "UNP", "RTX", "LMT", "MMM",
    "ETN", "PH", "WM", "FDX", "NSC", "ITW", "GD", "EMR", "JCI", "CMI"
]

TELECOM_UTIL_TICKERS = [
    "VZ", "T", "TMUS", "CHTR", "DUK", "SO", "NEE", "AEP", "D", "EXC",
    "PEG", "XEL", "ED", "WEC", "EIX"
]

ALL_PUBLIC_TICKERS = sorted(set(
    TECH_TICKERS
    + FINANCE_TICKERS
    + HEALTHCARE_TICKERS
    + ENERGY_TICKERS
    + CONSUMER_TICKERS
    + INDUSTRIAL_TICKERS
    + TELECOM_UTIL_TICKERS
))