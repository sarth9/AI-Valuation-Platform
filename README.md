# AI Company Valuation Platform

A multi-mode AI valuation platform that estimates company value for:

- Public Companies
- Private Companies
- Startup / SaaS Companies

The project uses machine learning for public-company valuation and structured valuation logic for private and startup/SaaS estimation.

---

## Features

### Public Company Mode
- Predicts estimated market capitalization
- Uses trained machine learning model
- Supports sector and industry-aware prediction
- Includes public-company comparison using Yahoo Finance
- Displays chart for predicted vs actual market cap
- Provides simple explanation of prediction drivers

### Private Company Mode
- Estimates enterprise value
- Uses structured private-company valuation logic
- Produces valuation band and explanation

### Startup / SaaS Mode
- Estimates startup valuation
- Uses ARR-multiple style startup logic
- Considers growth, churn, retention, runway, and burn

### Product Features
- Multi-mode frontend UI
- Model info panel
- Backend health status
- Explanation section
- Public comparison chart
- Sample data autofill for all modes

---

## Tech Stack

### Backend
- Python
- FastAPI
- scikit-learn
- XGBoost
- yfinance
- joblib

### Frontend
- HTML
- CSS
- Vanilla JavaScript
- Chart.js

### ML / Data
- pandas
- numpy
- scikit-learn
- XGBoost
- Yahoo Finance data via `yfinance`

---

## Project Structure

```text
company-valuation-ai/
│
├── app/
│   ├── api/
│   │   ├── main.py
│   │   ├── comparison_service.py
│   │   ├── routes_public.py
│   │   ├── routes_private.py
│   │   ├── routes_startup.py
│   │   ├── schemas_common.py
│   │   ├── schemas_public.py
│   │   ├── schemas_private.py
│   │   ├── schemas_startup.py
│   │   ├── predictor_public.py
│   │   ├── predictor_private.py
│   │   └── predictor_startup.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── logger.py
│   │
│   ├── data/
│   ├── models/
│   ├── preprocessing/
│   └── utils/
│
├── data/
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── config.js
│
├── saved_models/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md