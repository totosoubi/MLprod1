from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression


BASE_DIR = Path(__file__).resolve().parent


def build_model():
    df = pd.read_csv(BASE_DIR / "houses.csv")
    features = df[["size", "nb_rooms", "garden"]]
    model = LinearRegression().fit(features, df["price"])
    joblib.dump(model, BASE_DIR / "regression.joblib")
    return model


if __name__ == "__main__":
    build_model()
