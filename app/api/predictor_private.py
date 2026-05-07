from app.core.logger import setup_logger


logger = setup_logger("predictor_private")


class PrivateModelService:
    def __init__(self):
        self.model_name = "Private Company Heuristic Model v1"

    def predict(self, input_data: dict) -> float:
        annual_revenue = input_data.get("annual_revenue", 0)
        ebitda = input_data.get("ebitda", 0)
        revenue_growth = input_data.get("revenue_growth", 0)
        total_debt = input_data.get("total_debt", 0)
        total_cash = input_data.get("total_cash", 0)
        employee_count = input_data.get("employee_count", 0)
        recurring_revenue_ratio = input_data.get("recurring_revenue_ratio", 0)

        revenue_multiple = 1.8

        if revenue_growth > 0.20:
            revenue_multiple += 1.2
        elif revenue_growth > 0.10:
            revenue_multiple += 0.6

        if recurring_revenue_ratio > 0.50:
            revenue_multiple += 0.8

        if ebitda > 0:
            revenue_multiple += 0.5

        if employee_count > 500:
            revenue_multiple += 0.2

        enterprise_value = annual_revenue * revenue_multiple
        enterprise_value += max(ebitda, 0) * 3.0
        enterprise_value += max(total_cash - total_debt, 0)

        logger.info("Private company valuation estimate generated.")
        return float(max(enterprise_value, 0.0))

    def generate_explanation(self, input_data: dict) -> list[str]:
        points = []

        if input_data.get("revenue_growth", 0) > 0.20:
            points.append("High growth increased the valuation multiple.")
        if input_data.get("ebitda", 0) > 0:
            points.append("Positive EBITDA supported a stronger enterprise value estimate.")
        if input_data.get("recurring_revenue_ratio", 0) > 0.50:
            points.append("Higher recurring revenue improved valuation quality.")
        if input_data.get("total_debt", 0) > input_data.get("total_cash", 0):
            points.append("Debt burden may have constrained the valuation estimate.")

        if not points:
            points.append("The estimate was driven primarily by revenue scale, growth, and balance sheet strength.")

        return points

    def get_band(self, value: float) -> str:
        if value < 10_000_000:
            return "Early-stage / small private business range"
        if value < 100_000_000:
            return "Lower middle-market range"
        if value < 500_000_000:
            return "Mid-market range"
        return "Upper private-company range"

    def get_model_info(self) -> dict:
        return {
            "company_type": "private_company",
            "model_name": self.model_name,
            "target_name": "enterprise_value",
            "target_transform": "none",
            "notes": [
                "This is a private-company valuation estimator v1.",
                "Uses heuristic logic until a stronger labeled private-company dataset is added.",
                "Best used as an indicative estimate, not a formal valuation opinion.",
            ],
        }


private_model_service = PrivateModelService()