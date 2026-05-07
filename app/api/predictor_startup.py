from app.core.logger import setup_logger


logger = setup_logger("predictor_startup")


class StartupModelService:
    def __init__(self):
        self.model_name = "Startup/SaaS Heuristic Model v1"

    def predict(self, input_data: dict) -> float:
        arr = input_data.get("arr", 0)
        revenue_growth = input_data.get("revenue_growth", 0)
        gross_margin = input_data.get("gross_margin", 0)
        churn_rate = input_data.get("churn_rate", 0)
        net_revenue_retention = input_data.get("net_revenue_retention", 0)
        burn_rate_monthly = input_data.get("burn_rate_monthly", 0)
        runway_months = input_data.get("runway_months", 0)
        funding_stage = input_data.get("funding_stage", "").lower()

        arr_multiple = 4.0

        if revenue_growth > 0.80:
            arr_multiple += 4.0
        elif revenue_growth > 0.40:
            arr_multiple += 2.0
        elif revenue_growth > 0.20:
            arr_multiple += 1.0

        if gross_margin > 0.70:
            arr_multiple += 1.0

        if churn_rate < 0.05:
            arr_multiple += 1.0
        elif churn_rate > 0.15:
            arr_multiple -= 1.0

        if net_revenue_retention > 1.10:
            arr_multiple += 1.0

        if runway_months < 12:
            arr_multiple -= 1.0

        if burn_rate_monthly > 0 and runway_months < 6:
            arr_multiple -= 1.0

        if "series b" in funding_stage or "series c" in funding_stage or "growth" in funding_stage:
            arr_multiple += 0.5

        estimated_value = arr * max(arr_multiple, 1.0)

        logger.info("Startup/SaaS valuation estimate generated.")
        return float(max(estimated_value, 0.0))

    def generate_explanation(self, input_data: dict) -> list[str]:
        points = []

        if input_data.get("revenue_growth", 0) > 0.40:
            points.append("High growth increased the ARR multiple.")
        if input_data.get("gross_margin", 0) > 0.70:
            points.append("Strong gross margins improved software-style valuation quality.")
        if input_data.get("churn_rate", 0) < 0.05:
            points.append("Low churn supported a stronger valuation estimate.")
        if input_data.get("net_revenue_retention", 0) > 1.10:
            points.append("Strong net revenue retention increased the estimate.")
        if input_data.get("runway_months", 0) < 12:
            points.append("Short runway reduced the valuation estimate due to financing risk.")

        if not points:
            points.append("The estimate was driven mainly by ARR scale, growth, retention, and runway quality.")

        return points

    def get_band(self, value: float) -> str:
        if value < 5_000_000:
            return "Early startup range"
        if value < 50_000_000:
            return "Seed / early venture range"
        if value < 250_000_000:
            return "Scaling startup range"
        return "Late-stage startup range"

    def get_model_info(self) -> dict:
        return {
            "company_type": "startup_saas",
            "model_name": self.model_name,
            "target_name": "valuation",
            "target_transform": "none",
            "notes": [
                "This is a startup/SaaS valuation estimator v1.",
                "Uses ARR-multiple-style logic adjusted by growth, churn, retention, and runway.",
                "Best used as a directional estimate, not a formal fundraise valuation.",
            ],
        }


startup_model_service = StartupModelService()