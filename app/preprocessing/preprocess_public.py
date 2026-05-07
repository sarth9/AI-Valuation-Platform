import os
import numpy as np
import pandas as pd


RAW_DATA_PATH = "data/public/raw_company_data.csv"
PROCESSED_DATA_PATH = "data/public/processed_company_data.csv"

NUMERIC_FEATURES = [
    "enterprise_value",
    "total_revenue",
    "ebitda",
    "net_income",
    "total_cash",
    "total_debt",
    "book_value",
    "current_ratio",
    "debt_to_equity",
    "return_on_assets",
    "return_on_equity",
    "gross_margins",
    "operating_margins",
    "profit_margins",
    "revenue_growth",
    "earnings_growth",
    "trailing_pe",
    "forward_pe",
    "price_to_book",
    "beta",
    "shares_outstanding",
]

CATEGORICAL_FEATURES = ["sector", "industry"]
TARGET_COLUMN = "market_cap"


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["cash_to_debt_ratio"] = df["total_cash"] / df["total_debt"].replace(0, np.nan)
    df["debt_to_revenue_ratio"] = df["total_debt"] / df["total_revenue"].replace(0, np.nan)
    df["ebitda_margin_calc"] = df["ebitda"] / df["total_revenue"].replace(0, np.nan)
    df["net_income_margin_calc"] = df["net_income"] / df["total_revenue"].replace(0, np.nan)
    df["enterprise_to_revenue"] = df["enterprise_value"] / df["total_revenue"].replace(0, np.nan)

    return df


def preprocess_data(input_path: str = RAW_DATA_PATH, output_path: str = PROCESSED_DATA_PATH) -> pd.DataFrame:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df = pd.read_csv(input_path)

    print("Original shape:", df.shape)

    df = df.dropna(subset=[TARGET_COLUMN])
    print("After dropping missing target:", df.shape)

    keep_columns = ["ticker", "company_name", TARGET_COLUMN] + NUMERIC_FEATURES + CATEGORICAL_FEATURES
    df = df[keep_columns]

    df = add_engineered_features(df)
    df = df.replace([np.inf, -np.inf], np.nan)

    numeric_columns = df.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        df[col] = df[col].fillna(df[col].median())

    for col in CATEGORICAL_FEATURES:
        df[col] = df[col].fillna("Unknown")

    df = df[df[TARGET_COLUMN] > 0]

    print("Final processed shape:", df.shape)
    print("\nMissing values:")
    print(df.isnull().sum())

    df.to_csv(output_path, index=False)
    print(f"\nSaved processed public data to: {output_path}")

    return df


if __name__ == "__main__":
    processed_df = preprocess_data()
    print(processed_df.head())