import os
import joblib
import pandas as pd


MODEL_DIR = "saved_models"


def load_artifacts():
    """
    Load saved model artifacts.
    """
    rf_model_path = os.path.join(MODEL_DIR, "random_forest_model.pkl")
    scaler_path = os.path.join(MODEL_DIR, "scaler.pkl")
    feature_columns_path = os.path.join(MODEL_DIR, "feature_columns.pkl")

    rf_model = joblib.load(rf_model_path)
    scaler = joblib.load(scaler_path)
    feature_columns = joblib.load(feature_columns_path)

    return rf_model, scaler, feature_columns


def predict_market_cap(input_data: dict) -> float:
    """
    Predict market cap from input feature dictionary.
    Uses Random Forest as default best model.
    """
    rf_model, _, feature_columns = load_artifacts()

    input_df = pd.DataFrame([input_data])

    # Ensure column order matches training
    input_df = input_df.reindex(columns=feature_columns, fill_value=0)

    prediction = rf_model.predict(input_df)[0]
    return float(prediction)


if __name__ == "__main__":
    sample_input = {
        "enterprise_value": 3000000000000,
        "total_revenue": 400000000000,
        "ebitda": 130000000000,
        "net_income": 100000000000,
        "total_cash": 60000000000,
        "total_debt": 110000000000,
        "book_value": 5.0,
        "current_ratio": 1.2,
        "debt_to_equity": 180.0,
        "return_on_assets": 0.22,
        "return_on_equity": 1.25,
        "gross_margins": 0.46,
        "operating_margins": 0.31,
        "profit_margins": 0.25,
        "revenue_growth": 0.08,
        "earnings_growth": 0.12,
        "trailing_pe": 28.0,
        "forward_pe": 26.0,
        "price_to_book": 42.0,
        "beta": 1.10,
        "shares_outstanding": 15000000000,
        "cash_to_debt_ratio": 0.55,
        "debt_to_revenue_ratio": 0.27,
        "ebitda_margin_calc": 0.325,
        "net_income_margin_calc": 0.25,
        "enterprise_to_revenue": 7.5,
    }

    predicted_market_cap = predict_market_cap(sample_input)
    print(f"Predicted market cap: {predicted_market_cap:,.2f}")