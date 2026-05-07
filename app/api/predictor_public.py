import json
import os

import joblib
import numpy as np
import pandas as pd

from app.core.config import settings
from app.core.logger import setup_logger


logger = setup_logger("predictor_public")


class PublicModelService:
    def __init__(self):
        self.model = None
        self.feature_columns = None
        self.model_name = "Unknown"

    def load_artifacts(self):
        public_model_dir = os.path.join(settings.MODEL_DIR, "public")

        model_path = os.path.join(public_model_dir, "best_model.pkl")
        feature_columns_path = os.path.join(public_model_dir, "feature_columns.pkl")
        metadata_path = os.path.join(public_model_dir, "model_metadata.json")

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        if not os.path.exists(feature_columns_path):
            raise FileNotFoundError(f"Feature columns file not found: {feature_columns_path}")

        self.model = joblib.load(model_path)
        self.feature_columns = joblib.load(feature_columns_path)

        if os.path.exists(metadata_path):
            with open(metadata_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
                self.model_name = metadata.get("best_model_name", "Unknown")

        logger.info("Public model artifacts loaded successfully.")

    def engineer_features(self, input_data: dict) -> dict:
        total_cash = input_data.get("total_cash", 0)
        total_debt = input_data.get("total_debt", 0)
        total_revenue = input_data.get("total_revenue", 0)
        ebitda = input_data.get("ebitda", 0)
        net_income = input_data.get("net_income", 0)
        enterprise_value = input_data.get("enterprise_value", 0)

        input_data["cash_to_debt_ratio"] = total_cash / total_debt if total_debt else 0
        input_data["debt_to_revenue_ratio"] = total_debt / total_revenue if total_revenue else 0
        input_data["ebitda_margin_calc"] = ebitda / total_revenue if total_revenue else 0
        input_data["net_income_margin_calc"] = net_income / total_revenue if total_revenue else 0
        input_data["enterprise_to_revenue"] = enterprise_value / total_revenue if total_revenue else 0

        return input_data

    def generate_explanation(self, input_data: dict) -> list[str]:
        explanation = []

        revenue_growth = input_data.get("revenue_growth", 0)
        profit_margins = input_data.get("profit_margins", 0)
        total_debt = input_data.get("total_debt", 0)
        total_revenue = input_data.get("total_revenue", 1)
        current_ratio = input_data.get("current_ratio", 0)
        beta = input_data.get("beta", 0)
        debt_ratio = total_debt / total_revenue if total_revenue else 0

        if revenue_growth > 0.10:
            explanation.append("Strong revenue growth likely increased the predicted valuation.")
        elif revenue_growth < 0:
            explanation.append("Negative revenue growth likely reduced the predicted valuation.")

        if profit_margins > 0.20:
            explanation.append("Healthy profit margins suggest strong profitability.")
        elif profit_margins < 0.05:
            explanation.append("Weak profit margins may have lowered the valuation estimate.")

        if debt_ratio > 0.8:
            explanation.append("High debt relative to revenue may have negatively impacted the prediction.")
        elif debt_ratio < 0.3:
            explanation.append("Low debt burden relative to revenue supports a healthier valuation.")

        if current_ratio > 1.5:
            explanation.append("Strong short-term liquidity likely supported the valuation.")
        elif current_ratio < 1.0:
            explanation.append("Weak short-term liquidity may have hurt the valuation estimate.")

        if beta > 1.5:
            explanation.append("Higher volatility risk may reduce investor confidence in valuation.")
        elif beta < 1.0:
            explanation.append("Lower beta suggests relatively stable market behavior.")

        if not explanation:
            explanation.append(
                "The valuation was driven by a balanced mix of revenue, profitability, leverage, and market risk."
            )

        return explanation

    def predict(self, input_data: dict) -> float:
        if self.model is None or self.feature_columns is None:
            raise RuntimeError("Public model artifacts are not loaded.")

        prepared_input = self.engineer_features(input_data.copy())
        prepared_input.setdefault("sector", "Unknown")
        prepared_input.setdefault("industry", "Unknown")

        input_df = pd.DataFrame([prepared_input])
        input_df = input_df.reindex(columns=self.feature_columns, fill_value=0)
        input_df = input_df.replace([np.inf, -np.inf], 0)

        pred_log = self.model.predict(input_df)[0]
        pred_raw = np.expm1(pred_log)
        pred_raw = max(float(pred_raw), 0.0)

        logger.info("Public prediction generated successfully.")
        return pred_raw

    def predict_with_explanation(self, input_data: dict) -> tuple[float, list[str]]:
        prediction = self.predict(input_data)
        explanation = self.generate_explanation(input_data)
        return prediction, explanation

    def get_model_info(self) -> dict:
        return {
            "company_type": "public_company",
            "model_name": self.model_name,
            "target_name": "market_cap",
            "target_transform": "log1p",
            "notes": [
                "Designed for public operating companies.",
                "Works best with public-company-style financial inputs.",
                "Prediction is an estimate, not financial advice.",
            ],
        }


public_model_service = PublicModelService()