import os
import numpy as np
import pandas as pd


RAW_DATA_PATH = "data/private/private_company_data.csv"
PROCESSED_DATA_PATH = "data/private/processed_private_company_data.csv"


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["cash_to_debt_ratio"] = df["total_cash"] / df["total_debt"].replace(0, np.nan)
    df["debt_to_assets_ratio"] = df["total_debt"] / df["total_assets"].replace(0, np.nan)
    df["revenue_per_employee"] = df["annual_revenue"] / df["employee_count"].replace(0, np.nan)
    df["equity_ratio"] = df["shareholders_equity"] / df["total_assets"].replace(0, np.nan)

    return df


def preprocess_data(input_path: str = RAW_DATA_PATH, output_path: str = PROCESSED_DATA_PATH) -> pd.DataFrame:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df = pd.read_csv(input_path)
    df = add_engineered_features(df)
    df = df.replace([np.inf, -np.inf], np.nan)

    numeric_columns = df.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        df[col] = df[col].fillna(df[col].median())

    text_columns = df.select_dtypes(exclude=[np.number]).columns
    for col in text_columns:
        df[col] = df[col].fillna("Unknown")

    df.to_csv(output_path, index=False)
    print(f"Saved processed private data to: {output_path}")
    return df


if __name__ == "__main__":
    processed_df = preprocess_data()
    print(processed_df.head())