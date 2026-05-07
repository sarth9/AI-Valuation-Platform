import json
import os
import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, RandomizedSearchCV, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from xgboost import XGBRegressor


DATA_PATH = "data/public/processed_company_data.csv"
MODEL_DIR = "saved_models/public"
TARGET_COLUMN = "market_cap"
DROP_COLUMNS = ["ticker", "company_name", TARGET_COLUMN]


def load_data(data_path: str = DATA_PATH) -> pd.DataFrame:
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found: {data_path}")
    return pd.read_csv(data_path)


def prepare_xy(df: pd.DataFrame):
    X = df.drop(columns=DROP_COLUMNS, errors="ignore")
    y = df[TARGET_COLUMN].copy()
    y_log = np.log1p(y)
    return X, y, y_log


def split_feature_types(X: pd.DataFrame):
    numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = X.select_dtypes(exclude=[np.number]).columns.tolist()
    return numeric_features, categorical_features


def build_preprocessor(numeric_features: list[str], categorical_features: list[str]) -> ColumnTransformer:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_features),
            ("cat", categorical_pipeline, categorical_features),
        ]
    )


def evaluate_predictions(model_name: str, y_true_raw, y_pred_raw) -> dict:
    mae = mean_absolute_error(y_true_raw, y_pred_raw)
    rmse = np.sqrt(mean_squared_error(y_true_raw, y_pred_raw))
    r2 = r2_score(y_true_raw, y_pred_raw)

    print(f"\n--- {model_name} Test Evaluation ---")
    print(f"MAE : {mae:,.2f}")
    print(f"RMSE: {rmse:,.2f}")
    print(f"R2  : {r2:.4f}")

    return {
        "model": model_name,
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
    }


def cross_validate_model(model_name: str, pipeline: Pipeline, X, y_log) -> dict:
    cv = KFold(n_splits=5, shuffle=True, random_state=42)

    cv_r2 = cross_val_score(pipeline, X, y_log, cv=cv, scoring="r2")
    cv_neg_mae = cross_val_score(pipeline, X, y_log, cv=cv, scoring="neg_mean_absolute_error")

    results = {
        "model": model_name,
        "cv_r2_mean": float(cv_r2.mean()),
        "cv_r2_std": float(cv_r2.std()),
        "cv_mae_log_mean": float((-cv_neg_mae).mean()),
    }

    print(f"\n--- {model_name} Cross-Validation ---")
    print(f"CV R2 Mean : {results['cv_r2_mean']:.4f}")
    print(f"CV R2 Std  : {results['cv_r2_std']:.4f}")
    print(f"CV MAE(log): {results['cv_mae_log_mean']:.4f}")

    return results


def build_models(preprocessor: ColumnTransformer) -> dict:
    return {
        "linear_regression": Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", LinearRegression()),
            ]
        ),
        "random_forest": Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", RandomForestRegressor(random_state=42)),
            ]
        ),
        "xgboost": Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", XGBRegressor(
                    objective="reg:squarederror",
                    n_estimators=300,
                    max_depth=6,
                    learning_rate=0.05,
                    subsample=0.9,
                    colsample_bytree=0.9,
                    random_state=42,
                )),
            ]
        ),
    }


def tune_random_forest(preprocessor: ColumnTransformer, X_train, y_train_log) -> Pipeline:
    pipe = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", RandomForestRegressor(random_state=42)),
        ]
    )

    param_grid = {
        "model__n_estimators": [200, 300, 500],
        "model__max_depth": [6, 10, 14, None],
        "model__min_samples_split": [2, 4, 8],
        "model__min_samples_leaf": [1, 2, 4],
    }

    search = RandomizedSearchCV(
        estimator=pipe,
        param_distributions=param_grid,
        n_iter=12,
        cv=5,
        scoring="r2",
        random_state=42,
        n_jobs=-1,
    )

    search.fit(X_train, y_train_log)
    print("\nBest Random Forest params:")
    print(search.best_params_)
    print(f"Best Random Forest CV score: {search.best_score_:.4f}")
    return search.best_estimator_


def tune_xgboost(preprocessor: ColumnTransformer, X_train, y_train_log) -> Pipeline:
    pipe = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", XGBRegressor(
                objective="reg:squarederror",
                random_state=42,
            )),
        ]
    )

    param_grid = {
        "model__n_estimators": [200, 300, 500],
        "model__max_depth": [3, 4, 6, 8],
        "model__learning_rate": [0.03, 0.05, 0.1],
        "model__subsample": [0.8, 0.9, 1.0],
        "model__colsample_bytree": [0.8, 0.9, 1.0],
    }

    search = RandomizedSearchCV(
        estimator=pipe,
        param_distributions=param_grid,
        n_iter=12,
        cv=5,
        scoring="r2",
        random_state=42,
        n_jobs=-1,
    )

    search.fit(X_train, y_train_log)
    print("\nBest XGBoost params:")
    print(search.best_params_)
    print(f"Best XGBoost CV score: {search.best_score_:.4f}")
    return search.best_estimator_


def evaluate_on_test(model_name: str, model, X_test, y_test_raw):
    y_pred_log = model.predict(X_test)
    y_pred_raw = np.expm1(y_pred_log)
    y_pred_raw = np.maximum(y_pred_raw, 0)
    return evaluate_predictions(model_name, y_test_raw, y_pred_raw)


def save_artifacts(best_model, raw_feature_columns, metrics_summary, model_name: str):
    os.makedirs(MODEL_DIR, exist_ok=True)

    joblib.dump(best_model, os.path.join(MODEL_DIR, "best_model.pkl"))
    joblib.dump(raw_feature_columns, os.path.join(MODEL_DIR, "feature_columns.pkl"))

    metadata = {
        "best_model_name": model_name,
        "metrics": metrics_summary,
        "target_transform": "log1p",
    }

    with open(os.path.join(MODEL_DIR, "model_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"\nSaved public best model and metadata to: {MODEL_DIR}")


def main():
    print("Loading processed public dataset...")
    df = load_data()

    X, y_raw, y_log = prepare_xy(df)
    numeric_features, categorical_features = split_feature_types(X)
    preprocessor = build_preprocessor(numeric_features, categorical_features)

    print(f"Dataset shape: {df.shape}")
    print(f"Numeric features: {len(numeric_features)}")
    print(f"Categorical features: {len(categorical_features)}")

    X_train, X_test, y_train_raw, y_test_raw, y_train_log, y_test_log = train_test_split(
        X, y_raw, y_log, test_size=0.2, random_state=42
    )

    base_models = build_models(preprocessor)

    cv_results = {}
    for name, model in base_models.items():
        cv_results[name] = cross_validate_model(name, model, X_train, y_train_log)

    tuned_rf = tune_random_forest(preprocessor, X_train, y_train_log)
    tuned_xgb = tune_xgboost(preprocessor, X_train, y_train_log)

    lr_model = base_models["linear_regression"].fit(X_train, y_train_log)
    metrics_lr = evaluate_on_test("Linear Regression", lr_model, X_test, y_test_raw)
    metrics_rf = evaluate_on_test("Tuned Random Forest", tuned_rf, X_test, y_test_raw)
    metrics_xgb = evaluate_on_test("Tuned XGBoost", tuned_xgb, X_test, y_test_raw)

    candidates = [
        ("Linear Regression", lr_model, metrics_lr),
        ("Tuned Random Forest", tuned_rf, metrics_rf),
        ("Tuned XGBoost", tuned_xgb, metrics_xgb),
    ]

    best_name, best_model, best_metrics = max(candidates, key=lambda x: x[2]["r2"])

    print("\n=== Final Best Model ===")
    print(best_name)
    print(best_metrics)

    save_artifacts(
        best_model=best_model,
        raw_feature_columns=X.columns.tolist(),
        metrics_summary={
            "cv_results": cv_results,
            "test_results": {
                "linear_regression": metrics_lr,
                "tuned_random_forest": metrics_rf,
                "tuned_xgboost": metrics_xgb,
            },
        },
        model_name=best_name,
    )


if __name__ == "__main__":
    main()