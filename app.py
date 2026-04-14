import pickle

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="CardioInsight",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

        :root {
            --canvas: #f4efe8;
            --surface: rgba(255, 251, 245, 0.92);
            --surface-strong: #fffdf9;
            --ink: #1d2a33;
            --muted: #60707a;
            --line: rgba(29, 42, 51, 0.10);
            --brand: #0f766e;
            --brand-deep: #115e59;
            --brand-soft: rgba(15, 118, 110, 0.10);
            --alert: #9a3412;
            --alert-bg: #fff3ea;
            --ok: #166534;
            --ok-bg: #eefaf1;
            --shadow: 0 24px 70px rgba(31, 42, 52, 0.10);
        }

        html, body, [class*="css"] {
            font-family: 'Manrope', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(15, 118, 110, 0.16), transparent 34%),
                radial-gradient(circle at top right, rgba(194, 99, 58, 0.14), transparent 26%),
                linear-gradient(180deg, #f7f2eb 0%, #f2ece3 100%);
            color: var(--ink);
        }

        .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 2.5rem;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .hero-card,
        .panel-card,
        .metric-card,
        .result-card {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 24px;
            box-shadow: var(--shadow);
            backdrop-filter: blur(12px);
        }

        .hero-card {
            position: relative;
            overflow: hidden;
            padding: 2.4rem;
            margin-bottom: 1.1rem;
        }

        .hero-card::after {
            content: "";
            position: absolute;
            right: -40px;
            bottom: -60px;
            width: 240px;
            height: 240px;
            background: radial-gradient(circle, rgba(15, 118, 110, 0.20), transparent 70%);
        }

        .eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.45rem 0.8rem;
            border-radius: 999px;
            background: var(--brand-soft);
            color: var(--brand-deep);
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .hero-title {
            margin: 1rem 0 0;
            max-width: 10ch;
            font-size: clamp(2.3rem, 4vw, 4.2rem);
            line-height: 0.98;
            letter-spacing: -0.05em;
            font-weight: 800;
        }

        .hero-copy {
            max-width: 58ch;
            margin: 1rem 0 0;
            color: var(--muted);
            line-height: 1.75;
            font-size: 1rem;
        }

        .metrics {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.9rem;
            margin-top: 1.6rem;
        }

        .metric-card {
            padding: 1rem 1.1rem;
            background: rgba(255, 255, 255, 0.74);
        }

        .metric-label {
            display: block;
            color: var(--muted);
            font-size: 0.8rem;
            margin-bottom: 0.3rem;
        }

        .metric-value {
            display: block;
            color: var(--ink);
            font-size: 1.05rem;
            font-weight: 800;
        }

        .panel-card {
            padding: 1.4rem;
            margin-bottom: 1rem;
        }

        .panel-title {
            margin: 0 0 0.35rem;
            font-size: 1.05rem;
            font-weight: 800;
            color: var(--ink);
        }

        .panel-copy {
            margin: 0;
            color: var(--muted);
            line-height: 1.65;
            font-size: 0.96rem;
        }

        .section-kicker {
            color: var(--brand-deep);
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 0.35rem;
        }

        .stNumberInput label,
        .stSelectbox label {
            color: var(--ink);
            font-weight: 700;
        }

        .stNumberInput [data-baseweb="input"],
        .stSelectbox [data-baseweb="select"] > div {
            border-radius: 16px;
            background: rgba(255, 252, 248, 0.96);
            border: 1px solid rgba(29, 42, 51, 0.12);
        }

        .stButton > button {
            width: 100%;
            min-height: 3.3rem;
            border: none;
            border-radius: 18px;
            background: linear-gradient(135deg, var(--brand) 0%, #155e75 100%);
            color: #ffffff;
            font-size: 1rem;
            font-weight: 800;
            box-shadow: 0 18px 36px rgba(15, 118, 110, 0.25);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 22px 42px rgba(15, 118, 110, 0.30);
        }

        .result-card {
            padding: 1.45rem;
            margin-top: 0.5rem;
        }

        .result-card.high {
            background: linear-gradient(180deg, #fff8f3 0%, var(--alert-bg) 100%);
            border-color: rgba(154, 52, 18, 0.16);
        }

        .result-card.low {
            background: linear-gradient(180deg, #f8fffb 0%, var(--ok-bg) 100%);
            border-color: rgba(22, 101, 52, 0.16);
        }

        .result-badge {
            display: inline-block;
            padding: 0.4rem 0.7rem;
            border-radius: 999px;
            font-size: 0.77rem;
            font-weight: 800;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 0.75rem;
        }

        .high .result-badge {
            background: rgba(154, 52, 18, 0.10);
            color: var(--alert);
        }

        .low .result-badge {
            background: rgba(22, 101, 52, 0.10);
            color: var(--ok);
        }

        .result-title {
            margin: 0;
            font-size: 1.6rem;
            font-weight: 800;
            letter-spacing: -0.03em;
        }

        .high .result-title {
            color: var(--alert);
        }

        .low .result-title {
            color: var(--ok);
        }

        .result-copy {
            margin: 0.75rem 0 0;
            color: var(--muted);
            line-height: 1.7;
        }

        .stCaption {
            color: var(--muted);
        }

        @media (max-width: 900px) {
            .hero-card {
                padding: 1.5rem;
            }

            .metrics {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def load_assets():
    with open("heart_disease_model.pkl", "rb") as file:
        model = pickle.load(file)

    with open("model_columns.pkl", "rb") as file:
        model_columns = pickle.load(file)

    return model, model_columns


def build_input_frame(
    model_columns,
    age: int,
    trestbps: int,
    chol: int,
    thalch: int,
    oldpeak: float,
    sex: str,
    chest_pain: str,
    exercise_angina: str,
):
    input_data = pd.DataFrame(0, index=[0], columns=model_columns)
    input_data["age"] = age
    input_data["trestbps"] = trestbps
    input_data["chol"] = chol
    input_data["thalch"] = thalch
    input_data["oldpeak"] = oldpeak

    if "sex_Male" in input_data.columns:
        input_data["sex_Male"] = 1 if sex == "Male" else 0

    chest_pain_map = {
        "Atypical Angina": "cp_atypical angina",
        "Non-Anginal Pain": "cp_non-anginal",
        "Typical Angina": "cp_typical angina",
    }
    selected_cp_column = chest_pain_map.get(chest_pain)
    if selected_cp_column and selected_cp_column in input_data.columns:
        input_data[selected_cp_column] = 1

    if "exang_True" in input_data.columns:
        input_data["exang_True"] = 1 if exercise_angina == "Yes" else 0

    return input_data


def render_result(prediction: int, sex: str, chest_pain: str, exercise_angina: str) -> None:
    if prediction == 1:
        st.markdown(
            f"""
            <section class="result-card high">
                <div class="result-badge">Predicted Outcome</div>
                <h2 class="result-title">Higher risk profile detected</h2>
                <p class="result-copy">
                    The current screening pattern aligns with a higher likelihood of heart disease.
                    The selected profile includes <strong>{sex.lower()}</strong> patient data,
                    chest pain noted as <strong>{chest_pain.lower()}</strong>, and exercise-induced
                    angina marked <strong>{exercise_angina.lower()}</strong>. This result should be
                    treated as decision support and followed by clinical review.
                </p>
            </section>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <section class="result-card low">
                <div class="result-badge">Predicted Outcome</div>
                <h2 class="result-title">Lower risk profile detected</h2>
                <p class="result-copy">
                    The current screening pattern aligns with a lower likelihood of heart disease.
                    The selected profile includes <strong>{sex.lower()}</strong> patient data,
                    chest pain noted as <strong>{chest_pain.lower()}</strong>, and exercise-induced
                    angina marked <strong>{exercise_angina.lower()}</strong>. Continue using formal
                    evaluation and physician judgment where appropriate.
                </p>
            </section>
            """,
            unsafe_allow_html=True,
        )


inject_styles()
model, model_columns = load_assets()

st.markdown(
    """
    <section class="hero-card">
        <div class="eyebrow">Clinical Decision Support</div>
        <h1 class="hero-title">Professional heart disease screening experience.</h1>
        <p class="hero-copy">
            CardioInsight presents your model in a cleaner, more trustworthy interface with
            structured patient intake, polished visual hierarchy, and a results area designed
            to feel credible during demos, reviews, and portfolio presentations.
        </p>
        <div class="metrics">
            <div class="metric-card">
                <span class="metric-label">Prediction Type</span>
                <span class="metric-value">Binary heart disease risk</span>
            </div>
            <div class="metric-card">
                <span class="metric-label">Signal Categories</span>
                <span class="metric-value">Vitals, pain type, exercise response</span>
            </div>
            <div class="metric-card">
                <span class="metric-label">Positioning</span>
                <span class="metric-value">AI-assisted screening only</span>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

left_col, right_col = st.columns([1.4, 0.95], gap="large")

with left_col:
    st.markdown(
        """
        <section class="panel-card">
            <div class="section-kicker">Patient Intake</div>
            <h3 class="panel-title">Enter clinical indicators</h3>
            <p class="panel-copy">
                Complete the fields below to generate a prediction using the trained heart disease model.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        age = st.number_input("Age", min_value=1, max_value=120, value=50)
        trestbps = st.number_input("Resting Blood Pressure", min_value=50, max_value=250, value=120)
        chol = st.number_input("Cholesterol", min_value=100, max_value=600, value=200)
        sex = st.selectbox("Sex", ["Male", "Female"])

    with col_b:
        thalch = st.number_input("Maximum Heart Rate", min_value=50, max_value=220, value=150)
        oldpeak = st.number_input("Oldpeak (ST depression)", min_value=0.0, max_value=10.0, value=1.0)
        chest_pain = st.selectbox(
            "Chest Pain Type",
            ["Asymptomatic", "Atypical Angina", "Non-Anginal Pain", "Typical Angina"],
        )
        exercise_angina = st.selectbox("Exercise-Induced Angina", ["No", "Yes"])

    st.caption(
        "This interface is designed for screening support and presentation use. It is not a substitute for medical diagnosis."
    )
    analyze = st.button("Analyze Patient Risk")

with right_col:
    st.markdown(
        """
        <section class="panel-card">
            <div class="section-kicker">Model Notes</div>
            <h3 class="panel-title">Now aligned with saved model features</h3>
            <p class="panel-copy">
                The prediction input now matches the trained schema exactly, including one-hot encoded
                chest pain categories and exercise-induced angina. This removes the feature-name error
                that was crashing the app.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <section class="panel-card">
            <div class="section-kicker">Expected Inputs</div>
            <h3 class="panel-title">Included by the model</h3>
            <p class="panel-copy">
                Age, resting blood pressure, cholesterol, maximum heart rate, oldpeak, sex,
                chest pain category, and exercise-induced angina.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

if analyze:
    input_data = build_input_frame(
        model_columns=model_columns,
        age=age,
        trestbps=trestbps,
        chol=chol,
        thalch=thalch,
        oldpeak=oldpeak,
        sex=sex,
        chest_pain=chest_pain,
        exercise_angina=exercise_angina,
    )

    prediction = model.predict(input_data)
    render_result(int(prediction[0]), sex, chest_pain, exercise_angina)
