import os
import numpy as np
import pandas as pd


OUTPUT_DIR = "data/startup"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "startup_company_data.csv")


SECTORS = ["Technology", "Fintech", "Healthtech", "Edtech", "SaaS"]
BUSINESS_MODELS = ["B2B SaaS", "B2C SaaS", "Marketplace", "Subscription", "Fintech SaaS"]
FUNDING_STAGES = ["Pre-Seed", "Seed", "Series A", "Series B", "Series C"]
COUNTRIES = ["India", "USA", "UK", "Singapore", "Germany"]


def generate_startup_dataset(n_rows: int = 500, random_state: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)

    rows = []

    for _ in range(n_rows):
        arr = rng.uniform(100_000, 50_000_000)
        mrr = arr / 12
        revenue_growth = rng.uniform(0.05, 2.0)
        gross_margin = rng.uniform(0.40, 0.90)
        burn_rate_monthly = rng.uniform(20_000, 1_000_000)
        runway_months = rng.uniform(3, 36)
        customer_count = int(rng.integers(10, 20_000))
        churn_rate = rng.uniform(0.01, 0.25)
        net_revenue_retention = rng.uniform(0.80, 1.40)
        employee_count = int(rng.integers(5, 600))
        cac = rng.uniform(200, 20_000)
        ltv = rng.uniform(1_000, 150_000)
        logo_retention = rng.uniform(0.70, 0.98)
        active_users = int(rng.integers(500, 1_000_000))
        arpu = rng.uniform(100, 10_000)

        arr_multiple = 3.5
        arr_multiple += 3.0 if revenue_growth > 1.0 else 1.5 if revenue_growth > 0.5 else 0.5
        arr_multiple += 1.0 if gross_margin > 0.70 else 0.0
        arr_multiple += 1.0 if churn_rate < 0.05 else -1.0 if churn_rate > 0.15 else 0.0
        arr_multiple += 1.0 if net_revenue_retention > 1.10 else 0.0
        arr_multiple -= 1.0 if runway_months < 12 else 0.0

        valuation = arr * max(arr_multiple, 1.0)
        valuation *= rng.uniform(0.85, 1.15)

        rows.append({
            "sector": rng.choice(SECTORS),
            "business_model": rng.choice(BUSINESS_MODELS),
            "funding_stage": rng.choice(FUNDING_STAGES),
            "country": rng.choice(COUNTRIES),
            "arr": arr,
            "mrr": mrr,
            "revenue_growth": revenue_growth,
            "gross_margin": gross_margin,
            "burn_rate_monthly": burn_rate_monthly,
            "runway_months": runway_months,
            "customer_count": customer_count,
            "churn_rate": churn_rate,
            "net_revenue_retention": net_revenue_retention,
            "employee_count": employee_count,
            "cac": cac,
            "ltv": ltv,
            "logo_retention": logo_retention,
            "active_users": active_users,
            "arpu": arpu,
            "valuation": max(valuation, 250_000),
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = generate_startup_dataset()
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved synthetic startup dataset to: {OUTPUT_FILE}")
    print(df.head())