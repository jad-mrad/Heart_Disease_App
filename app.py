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
        @import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;500;600;700&display=swap');

        :root {
            --bg: #eef3f1;
            --bg-glow: rgba(122, 156, 146, 0.14);
            --surface: rgba(252, 253, 252, 0.92);
            --surface-strong: #ffffff;
            --text: #1f2f2c;
            --muted: #617571;
            --line: rgba(54, 84, 78, 0.12);
            --brand: #5c8c82;
            --brand-deep: #486f67;
            --brand-soft: #e1ece8;
            --success: #3f7b61;
            --success-bg: #edf7f1;
            --warning: #9a6a43;
            --warning-bg: #fcf4ed;
            --shadow: 0 20px 50px rgba(40, 61, 58, 0.08);
        }

        html, body, [class*="css"] {
            font-family: 'Source Sans 3', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, var(--bg-glow), transparent 32%),
                radial-gradient(circle at bottom right, rgba(186, 199, 192, 0.18), transparent 28%),
                linear-gradient(180deg, #f4f7f6 0%, var(--bg) 100%);
            color: var(--text);
        }

        .block-container {
            max-width: 1180px;
            padding-top: 1.8rem;
            padding-bottom: 2.4rem;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .hero-card,
        .info-card,
        .result-card {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 24px;
            box-shadow: var(--shadow);
            backdrop-filter: blur(8px);
        }

        .hero-card {
            padding: 2.2rem;
            margin-bottom: 1rem;
        }

        .hero-tag {
            display: inline-block;
            padding: 0.45rem 0.85rem;
            border-radius: 999px;
            background: var(--brand-soft);
            color: var(--brand-deep);
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .hero-title {
            margin: 0.9rem 0 0;
            font-size: clamp(2.2rem, 4vw, 4rem);
            line-height: 1.02;
            letter-spacing: -0.03em;
            font-weight: 700;
            max-width: 11ch;
        }

        .hero-copy {
            margin: 1rem 0 0;
            max-width: 60ch;
            color: var(--muted);
            font-size: 1.05rem;
            line-height: 1.7;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.9rem;
            margin-top: 1.5rem;
        }

        .feature-chip {
            background: rgba(255, 255, 255, 0.72);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 1rem 1.05rem;
        }

        .feature-label {
            display: block;
            margin-bottom: 0.25rem;
            color: var(--muted);
            font-size: 0.84rem;
        }

        .feature-value {
            display: block;
            font-size: 1rem;
            font-weight: 700;
            color: var(--text);
        }

        .info-card {
            padding: 1.35rem;
            margin-bottom: 1rem;
        }

        .card-kicker {
            color: var(--brand-deep);
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 0.35rem;
        }

        .card-title {
            margin: 0;
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--text);
        }

        .card-copy {
            margin: 0.55rem 0 0;
            color: var(--muted);
            font-size: 0.98rem;
            line-height: 1.65;
        }

        .stNumberInput label,
        .stSelectbox label {
            color: var(--text);
            font-weight: 600;
        }

        .stNumberInput [data-baseweb="input"],
        .stSelectbox [data-baseweb="select"] > div {
            background: var(--surface-strong);
            border: 1px solid rgba(54, 84, 78, 0.14);
            border-radius: 16px;
            min-height: 3rem;
        }

        .stNumberInput [data-baseweb="input"]:focus-within,
        .stSelectbox [data-baseweb="select"] > div:focus-within {
            border-color: rgba(92, 140, 130, 0.55);
            box-shadow: 0 0 0 3px rgba(92, 140, 130, 0.12);
        }

        .stButton > button {
            width: 100%;
            min-height: 3.2rem;
            border: none;
            border-radius: 16px;
            background: linear-gradient(135deg, var(--brand) 0%, var(--brand-deep) 100%);
            color: #ffffff;
            font-size: 1rem;
            font-weight: 700;
            box-shadow: 0 14px 30px rgba(72, 111, 103, 0.18);
            transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 18px 36px rgba(72, 111, 103, 0.22);
            filter: brightness(1.02);
        }

        .stButton > button:focus {
            outline: 3px solid rgba(92, 140, 130, 0.24);
            outline-offset: 2px;
        }

        .result-card {
            padding: 1.35rem;
            margin-top: 0.5rem;
        }

        .result-card.high {
            background: linear-gradient(180deg, #fffdfa 0%, var(--warning-bg) 100%);
            border-color: rgba(154, 106, 67, 0.18);
        }

        .result-card.low {
            background: linear-gradient(180deg, #fcfffd 0%, var(--success-bg) 100%);
            border-color: rgba(63, 123, 97, 0.18);
        }

        .result-badge {
            display: inline-block;
            padding: 0.38rem 0.72rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            margin-bottom: 0.75rem;
        }

        .high .result-badge {
            background: rgba(154, 106, 67, 0.10);
            color: var(--warning);
        }

        .low .result-badge {
            background: rgba(63, 123, 97, 0.10);
            color: var(--success);
        }

        .result-title {
            margin: 0;
            font-size: 1.55rem;
            line-height: 1.15;
            font-weight: 700;
        }

        .high .result-title {
            color: var(--warning);
        }

        .low .result-title {
            color: var(--success);
        }

        .result-copy {
            margin: 0.7rem 0 0;
            color: var(--muted);
            line-height: 1.7;
            font-size: 1rem;
        }

        .stCaption {
            color: var(--muted);
            font-size: 0.95rem;
        }

        @media (max-width: 900px) {
            .hero-card {
                padding: 1.5rem;
            }

            .feature-grid {
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
                <div class="result-badge">Screening Result</div>
                <h2 class="result-title">Higher risk pattern detected</h2>
                <p class="result-copy">
                    The entered values match a pattern that this model associates with a higher
                    likelihood of heart disease. This result uses <strong>{sex.lower()}</strong>
                    patient data, a chest pain profile of <strong>{chest_pain.lower()}</strong>,
                    and exercise-induced angina marked <strong>{exercise_angina.lower()}</strong>.
                    Please treat this as a supportive screening result, not a diagnosis.
                </p>
            </section>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <section class="result-card low">
                <div class="result-badge">Screening Result</div>
                <h2 class="result-title">Lower risk pattern detected</h2>
                <p class="result-copy">
                    The entered values match a pattern that this model associates with a lower
                    likelihood of heart disease. This result uses <strong>{sex.lower()}</strong>
                    patient data, a chest pain profile of <strong>{chest_pain.lower()}</strong>,
                    and exercise-induced angina marked <strong>{exercise_angina.lower()}</strong>.
                    Clinical judgment and proper medical evaluation should still guide decisions.
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
        <div class="hero-tag">Accessible Clinical Screening</div>
        <h1 class="hero-title">A softer, clearer heart risk screening experience.</h1>
        <p class="hero-copy">
            CardioInsight is designed to feel calm, professional, and easy to use. The page uses
            softer colors, readable spacing, and simple wording so more people can review patient
            information comfortably.
        </p>
        <div class="feature-grid">
            <div class="feature-chip">
                <span class="feature-label">Visual Style</span>
                <span class="feature-value">Soft contrast and low eye strain</span>
            </div>
            <div class="feature-chip">
                <span class="feature-label">Language</span>
                <span class="feature-value">Clear labels for broader usability</span>
            </div>
            <div class="feature-chip">
                <span class="feature-label">Use Case</span>
                <span class="feature-value">AI-assisted screening support</span>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

left_col, right_col = st.columns([1.45, 0.95], gap="large")

with left_col:
    st.markdown(
        """
        <section class="info-card">
            <div class="card-kicker">Patient Form</div>
            <h3 class="card-title">Enter patient information</h3>
            <p class="card-copy">
                Fill in the details below to create a heart disease screening result from the trained model.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    form_left, form_right = st.columns(2, gap="large")

    with form_left:
        age = st.number_input("Age", min_value=1, max_value=120, value=50)
        trestbps = st.number_input("Resting blood pressure", min_value=50, max_value=250, value=120)
        chol = st.number_input("Cholesterol", min_value=100, max_value=600, value=200)
        sex = st.selectbox("Sex", ["Male", "Female"])

    with form_right:
        thalch = st.number_input("Maximum heart rate", min_value=50, max_value=220, value=150)
        oldpeak = st.number_input("Oldpeak (ST depression)", min_value=0.0, max_value=10.0, value=1.0)
        chest_pain = st.selectbox(
            "Chest pain type",
            ["Asymptomatic", "Atypical Angina", "Non-Anginal Pain", "Typical Angina"],
        )
        exercise_angina = st.selectbox("Exercise-induced angina", ["No", "Yes"])

    st.caption(
        "This tool supports screening only. It should not replace medical diagnosis or professional advice."
    )
    analyze = st.button("Analyze Patient Risk")

with right_col:
    st.markdown(
        """
        <section class="info-card">
            <div class="card-kicker">Design Focus</div>
            <h3 class="card-title">Made for comfort and clarity</h3>
            <p class="card-copy">
                This version uses softer colors, larger breathing room, clearer text, and gentler result
                panels so the interface feels more trustworthy and less tiring to look at.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <section class="info-card">
            <div class="card-kicker">Model Inputs</div>
            <h3 class="card-title">Fields used by the model</h3>
            <p class="card-copy">
                Age, resting blood pressure, cholesterol, maximum heart rate, oldpeak,
                sex, chest pain type, and exercise-induced angina.
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
