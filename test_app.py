import math
from pathlib import Path
import unittest

import joblib
import pandas as pd
from fastapi.testclient import TestClient
from streamlit.testing.v1 import AppTest

from main import app


BASE_DIR = Path(__file__).resolve().parent


class PredictionTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.features = {"size": 120.0, "nb_rooms": 3, "garden": 1}

    def test_prediction_matches_model(self):
        expected = float(
            joblib.load(BASE_DIR / "regression.joblib")
            .predict(pd.DataFrame([self.features]))[0]
        )
        self.assertTrue(math.isfinite(expected))
        for response in (
            self.client.get("/predict", params=self.features),
            self.client.post("/predict", json=self.features),
        ):
            self.assertEqual(response.status_code, 200)
            self.assertAlmostEqual(response.json()["y_pred"], expected)

    def test_invalid_features_return_422(self):
        for field, value in (
            ("size", -1), ("size", "nan"), ("size", "inf"),
            ("nb_rooms", -1), ("nb_rooms", 1.5), ("garden", 2),
        ):
            features = {**self.features, field: value}
            with self.subTest(field=field, value=value):
                self.assertEqual(
                    self.client.get("/predict", params=features).status_code, 422
                )
                self.assertEqual(
                    self.client.post("/predict", json=features).status_code, 422
                )

    def test_missing_feature_returns_422(self):
        self.assertEqual(self.client.post("/predict", json={}).status_code, 422)

    def test_streamlit_prediction(self):
        app_test = AppTest.from_file(str(BASE_DIR / "model_app.py"))
        app_test.run(timeout=30)
        self.assertEqual(len(app_test.exception), 0)
        self.assertEqual(len(app_test.number_input), 3)
        self.assertEqual(len(app_test.metric), 0)
        app_test.number_input[0].set_value(150.0)
        app_test.button[0].click().run(timeout=30)
        self.assertEqual(len(app_test.exception), 0)
        expected = self.client.post(
            "/predict", json={**self.features, "size": 150.0}
        ).json()["y_pred"]
        formatted = f"{expected:,.0f} EUR".replace(",", " ")
        self.assertEqual(app_test.metric[0].value, formatted)
        self.assertEqual(len(app_test.json), 1)


if __name__ == "__main__":
    unittest.main()
