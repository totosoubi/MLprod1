from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "regression.joblib"

app = FastAPI(title="House Price Prediction API")
model = joblib.load(MODEL_PATH)


class HouseFeatures(BaseModel):
    size: float = Field(..., ge=0)
    nb_rooms: int = Field(..., ge=0)
    garden: int = Field(..., ge=0, le=1)


def predict_price(features: HouseFeatures) -> float:
    row = pd.DataFrame(
        [
            {
                "size": features.size,
                "nb_rooms": features.nb_rooms,
                "garden": features.garden,
            }
        ]
    )
    return float(model.predict(row)[0])


@app.get("/")
def read_root():
    return {"message": "Use /predict for house price predictions."}


@app.get("/predict")
def predict_get(size: float = 120.0, nb_rooms: int = 3, garden: int = 1):
    features = HouseFeatures(size=size, nb_rooms=nb_rooms, garden=garden)
    return {"y_pred": predict_price(features)}


@app.post("/predict")
def predict_post(features: HouseFeatures):
    return {"y_pred": predict_price(features)}
