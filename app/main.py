from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from enum import Enum
import pandas as pd
import xgboost as xgb
import pickle
import tempfile
from google.cloud import storage

app = FastAPI()

# Your GCP project and bucket info
PROJECT_ID = "top-broker-468417-b8"
BUCKET_NAME = "penguinmodels"
MODEL_BLOB_NAME = "xgb_penguin_model.json"
LABEL_ENCODER_BLOB_NAME = "label_encoder.pkl"

def download_blob_to_tempfile(bucket_name, blob_name, project_id):
    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    blob.download_to_filename(tmp_file.name)
    return tmp_file.name

# Download model and label encoder from GCS
MODEL_PATH = download_blob_to_tempfile(BUCKET_NAME, MODEL_BLOB_NAME, PROJECT_ID)
LABEL_ENCODER_PATH = download_blob_to_tempfile(BUCKET_NAME, LABEL_ENCODER_BLOB_NAME, PROJECT_ID)

# Load the trained XGBoost model
model = xgb.Booster()
model.load_model(MODEL_PATH)

# Load label encoder
with open(LABEL_ENCODER_PATH, "rb") as f:
    le = pickle.load(f)

class SexEnum(str, Enum):
    Male = "Male"
    Female = "Female"

class IslandEnum(str, Enum):
    Biscoe = "Biscoe"
    Dream = "Dream"
    Torgersen = "Torgersen"

class PenguinFeatures(BaseModel):
    bill_length_mm: float = Field(..., gt=0)
    bill_depth_mm: float = Field(..., gt=0)
    flipper_length_mm: float = Field(..., gt=0)
    body_mass_g: float = Field(..., gt=0)
    sex: SexEnum
    island: IslandEnum

expected_cols = [
    'bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g',
    'sex_Female', 'sex_Male',
    'island_Biscoe', 'island_Dream', 'island_Torgersen'
]

@app.post("/predict")
def predict_species(features: PenguinFeatures):
    try:
        df = pd.DataFrame([features.model_dump()])
        df = pd.get_dummies(df, columns=['sex', 'island'])
        for col in expected_cols:
            if col not in df.columns:
                df[col] = 0
        df = df[expected_cols]

        dmatrix = xgb.DMatrix(df)
        pred_numeric = model.predict(dmatrix)[0]
        pred_species = le.inverse_transform([int(pred_numeric)])[0]

        return {"predicted_species": pred_species}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")
