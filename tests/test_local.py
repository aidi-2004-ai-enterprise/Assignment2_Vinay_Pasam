# tests/test_main.py

import sys
import os
import pytest
import pandas as pd
import xgboost as xgb
from fastapi.testclient import TestClient

# Add project root to sys.path for imports if needed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import from app.main only (since main.py is inside app folder)
from app.main import app, model, le, expected_cols

client = TestClient(app)

VALID_PENGUIN = {
    "bill_length_mm": 39.1,
    "bill_depth_mm": 18.7,
    "flipper_length_mm": 181.0,
    "body_mass_g": 3750.0,
    "sex": "Male",
    "island": "Torgersen"
}

def _prepare_df_for_model(payload):
    df = pd.DataFrame([payload])
    df = pd.get_dummies(df, columns=['sex', 'island'])
    for col in expected_cols:
        if col not in df.columns:
            df[col] = 0
    df = df[expected_cols]
    return df

def test_model_prediction_direct():
    df = _prepare_df_for_model(VALID_PENGUIN)
    dmatrix = xgb.DMatrix(df)
    preds = model.predict(dmatrix)
    assert len(preds) == 1
    pred_idx = int(preds[0])
    label = le.inverse_transform([pred_idx])[0]
    assert isinstance(label, str)
    assert label in list(le.classes_)

def test_api_predict_endpoint_ok():
    resp = client.post("/predict", json=VALID_PENGUIN)
    assert resp.status_code == 200
    data = resp.json()
    assert "predicted_species" in data
    assert isinstance(data["predicted_species"], str)

def test_missing_field_returns_422():
    bad = VALID_PENGUIN.copy()
    bad.pop("bill_length_mm")
    resp = client.post("/predict", json=bad)
    assert resp.status_code == 422

def test_invalid_type_returns_422():
    bad = VALID_PENGUIN.copy()
    bad["bill_length_mm"] = "not_a_number"
    resp = client.post("/predict", json=bad)
    assert resp.status_code == 422

def test_negative_body_mass_returns_422():
    bad = VALID_PENGUIN.copy()
    bad["body_mass_g"] = -100.0
    resp = client.post("/predict", json=bad)
    assert resp.status_code == 422

def test_empty_request_returns_422():
    resp = client.post("/predict", json={})
    assert resp.status_code == 422

def test_extreme_values_return_label():
    extreme = VALID_PENGUIN.copy()
    extreme["body_mass_g"] = 999999.0
    resp = client.post("/predict", json=extreme)
    assert resp.status_code in (200, 400)
    if resp.status_code == 200:
        assert "predicted_species" in resp.json()
