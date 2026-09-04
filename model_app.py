import joblib
import pandas as pd
import streamlit as st


MODEL_PATH = "regression.joblib"

st.set_page_config(page_title="Prediction maison", layout="centered")


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


model = load_model()

st.markdown(
    """
    <style>
        .block-container {
            max-width: 760px;
            padding-top: 2rem;
        }
        h1 {
            font-size: 2.4rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0.25rem !important;
        }
        div[data-testid="stMetric"] {
            border: 1px solid rgba(128, 128, 128, 0.25);
            border-radius: 8px;
            padding: 1rem 1.25rem;
            background: rgba(128, 128, 128, 0.08);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Prix estime")
st.caption("Prediction du prix d'une maison")

with st.form("prediction_form"):
    col_size, col_rooms = st.columns(2)

    with col_size:
        size = st.number_input("Taille", min_value=0.0, value=120.0, step=1.0)

    with col_rooms:
        nb_rooms = st.number_input("Chambres", min_value=0, value=3, step=1)

    garden = st.number_input("Jardin", min_value=0, max_value=1, value=1, step=1)
    submitted = st.form_submit_button("Predire")

features = pd.DataFrame(
    [{"size": size, "nb_rooms": nb_rooms, "garden": garden}]
)

y_pred = model.predict(features)[0]

if submitted:
    st.write({"y_pred": float(y_pred)})
