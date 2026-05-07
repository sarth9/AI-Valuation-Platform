import os
import numpy as np
import pandas as pd


OUTPUT_DIR = "data/private"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "private_company_data.csv")


SECTORS = [
    "Technology",
    "Industrials",
    "Healthcare",
    "Financial Services",
    "Consumer",
    "Energy",
]

INDUSTRIES = [
    "Software",
    "Business Services",
    "Manufacturing",
    "Healthcare Services",
    "Retail",
    "Logistics",
]

COUNTRIES = ["India", "USA", "UK", "Germany", "Singapore"]


def generate_private_dataset(n_rows: int = 500, random_state: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)

    rows = []

    for _ in range(n_rows):
        annual_revenue = rng.uniform(5_000_000, 500_000_000)
        ebitda_margin = rng.uniform(0.05, 0.30)
        net_margin = rng.uniform(0.02, 0.18)

        ebitda = annual_revenue * ebitda_margin
        net_income = annual_revenue * net_margin

        total_cash = rng.uniform(500_000, 50_000_000)
        total_debt = rng.uniform(0, 80_000_000)
        total_assets = annual_revenue * rng.uniform(0.8, 2.5)
        total_liabilities = total_assets * rng.uniform(0.2, 0.7)
        shareholders_equity = total_assets - total_liabilities

        gross_margin = rng.uniform(0.20, 0.75)
        operating_margin = rng.uniform(0.05, 0.25)
        revenue_growth = rng.uniform(-0.05, 0.35)
        employee_count = int(rng.integers(20, 5000))
        company_age_years = rng.uniform(2, 40)

        free_cash_flow = ebitda * rng.uniform(0.4, 0.9)
        operating_cash_flow = ebitda * rng.uniform(0.7, 1.2)
        capex = annual_revenue * rng.uniform(0.01, 0.08)
        customer_count = int(rng.integers(10, 5000))
        recurring_revenue_ratio = rng.uniform(0.0, 0.9)

        revenue_multiple = 1.5
        revenue_multiple += 2.0 * max(revenue_growth, 0)
        revenue_multiple += 1.2 * recurring_revenue_ratio
        revenue_multiple += 0.5 if ebitda > 0 else -0.3
        revenue_multiple += 0.2 if employee_count > 500 else 0.0

        enterprise_value = annual_revenue * revenue_multiple
        enterprise_value += max(ebitda, 0) * 2.5
        enterprise_value += max(total_cash - total_debt, 0)
        enterprise_value *= rng.uniform(0.85, 1.15)

        rows.append({
            "sector": rng.choice(SECTORS),
            "industry": rng.choice(INDUSTRIES),
            "country": rng.choice(COUNTRIES),
            "annual_revenue": annual_revenue,
            "ebitda": ebitda,
            "net_income": net_income,
            "total_cash": total_cash,
            "total_debt": total_debt,
            "total_assets": total_assets,
            "total_liabilities": total_liabilities,
            "shareholders_equity": shareholders_equity,
            "gross_margin": gross_margin,
            "operating_margin": operating_margin,
            "net_margin": net_margin,
            "revenue_growth": revenue_growth,
            "employee_count": employee_count,
            "company_age_years": company_age_years,
            "free_cash_flow": free_cash_flow,
            "operating_cash_flow": operating_cash_flow,
            "capex": capex,
            "customer_count": customer_count,
            "recurring_revenue_ratio": recurring_revenue_ratio,
            "enterprise_value": max(enterprise_value, 1_000_000),
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = generate_private_dataset()
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved synthetic private dataset to: {OUTPUT_FILE}")
    print(df.head())