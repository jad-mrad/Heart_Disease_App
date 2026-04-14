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
        @import url('https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600;700;800&display=swap');

        :root {
            --bg: #edf2f6;
            --surface: rgba(255, 255, 255, 0.94);
            --surface-strong: #ffffff;
            --text: #173042;
            --muted: #607586;
            --line: #d8e3ec;
            --brand: #1f6f78;
            --brand-dark: #184f56;
            --brand-soft: #e6f2f3;
            --accent: #d97745;
            --ok: #22795d;
            --ok-soft: #eaf7f1;
            --warn: #a65d34;
            --warn-soft: #fdf1e9;
            --shadow: 0 22px 60px rgba(24, 43, 58, 0.08);
        }

        html, body, [class*="css"] {
            font-family: 'Public Sans', sans-serif;
            color: var(--text);
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(31, 111, 120, 0.08), transparent 28%),
                radial-gradient(circle at bottom right, rgba(217, 119, 69, 0.08), transparent 22%),
                linear-gradient(180deg, #f5f8fb 0%, var(--bg) 100%);
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 1.5rem;
            padding-bottom: 2.5rem;
        }

        .app-shell {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .topbar,
        .hero-panel,
        .section-panel,
        .side-panel,
        .result-panel {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 24px;
            box-shadow: var(--shadow);
        }

        .topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
            padding: 1rem 1.3rem;
        }

        .brand-wrap {
            display: flex;
            align-items: center;
            gap: 0.9rem;
        }

        .brand-mark {
            width: 46px;
            height: 46px;
            border-radius: 14px;
            display: grid;
            place-items: center;
            background: linear-gradient(135deg, var(--brand) 0%, var(--brand-dark) 100%);
            color: white;
            font-size: 1.2rem;
            font-weight: 800;
        }

        .brand-title {
            margin: 0;
            font-size: 1.05rem;
            font-weight: 800;
            color: var(--text);
        }

        .brand-copy {
            margin: 0.15rem 0 0;
            color: var(--muted);
            font-size: 0.94rem;
        }

        .topbar-badge {
            padding: 0.5rem 0.8rem;
            border-radius: 999px;
            background: var(--brand-soft);
            color: var(--brand-dark);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .hero-panel {
            padding: 2rem;
            background:
                linear-gradient(135deg, rgba(31, 111, 120, 0.06) 0%, rgba(255, 255, 255, 0.96) 52%),
                linear-gradient(180deg, #ffffff 0%, #f8fbfd 100%);
        }

        .eyebrow {
            display: inline-block;
            padding: 0.42rem 0.74rem;
            border-radius: 999px;
            background: var(--brand-soft);
            color: var(--brand-dark);
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .hero-title {
            margin: 0.9rem 0 0;
            max-width: 12ch;
            font-size: clamp(2.4rem, 4vw, 4.4rem);
            line-height: 0.98;
            letter-spacing: -0.04em;
            font-weight: 800;
            color: var(--text);
        }

        .hero-copy {
            margin: 1rem 0 0;
            max-width: 62ch;
            color: var(--muted);
            font-size: 1.06rem;
            line-height: 1.75;
        }

        .hero-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.9rem;
            margin-top: 1.6rem;
        }

        .hero-stat {
            padding: 1rem 1.05rem;
            border: 1px solid var(--line);
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.82);
        }

        .hero-stat-label {
            display: block;
            color: var(--muted);
            font-size: 0.82rem;
            margin-bottom: 0.25rem;
        }

        .hero-stat-value {
            display: block;
            color: var(--text);
            font-size: 1rem;
            font-weight: 700;
        }

        .section-panel,
        .side-panel,
        .result-panel {
            padding: 1.35rem;
        }

        .section-kicker {
            color: var(--brand);
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 0.35rem;
        }

        .section-title {
            margin: 0;
            font-size: 1.2rem;
            font-weight: 800;
            color: var(--text);
        }

        .section-copy {
            margin: 0.55rem 0 0;
            color: var(--muted);
            font-size: 0.97rem;
            line-height: 1.7;
        }

        .field-help {
            margin-top: -0.3rem;
            margin-bottom: 0.4rem;
            color: var(--muted);
            font-size: 0.86rem;
        }

        .step-card {
            padding: 1rem 1.05rem;
            border-radius: 18px;
            border: 1px solid var(--line);
            background: #fbfdff;
            margin-bottom: 0.85rem;
        }

        .step-number {
            display: inline-grid;
            place-items: center;
            width: 28px;
            height: 28px;
            border-radius: 999px;
            background: var(--brand-soft);
            color: var(--brand-dark);
            font-size: 0.85rem;
            font-weight: 800;
            margin-bottom: 0.55rem;
        }

        .step-title {
            margin: 0;
            font-size: 1rem;
            font-weight: 700;
            color: var(--text);
        }

        .step-copy {
            margin: 0.4rem 0 0;
            color: var(--muted);
            font-size: 0.94rem;
            line-height: 1.65;
        }

        .stNumberInput label,
        .stSelectbox label {
            color: var(--text);
            font-weight: 700;
            font-size: 0.97rem;
        }

        .stNumberInput [data-baseweb="input"],
        .stSelectbox [data-baseweb="select"] > div {
            background: var(--surface-strong);
            border: 1px solid var(--line);
            border-radius: 16px;
            min-height: 3.1rem;
        }

        .stNumberInput [data-baseweb="input"]:focus-within,
        .stSelectbox [data-baseweb="select"] > div:focus-within {
            border-color: rgba(31, 111, 120, 0.55);
            box-shadow: 0 0 0 3px rgba(31, 111, 120, 0.12);
        }

        .stButton > button {
            width: 100%;
            min-height: 3.3rem;
            border: none;
            border-radius: 18px;
            background: linear-gradient(135deg, var(--brand) 0%, var(--brand-dark) 100%);
            color: #ffffff;
            font-size: 1rem;
            font-weight: 800;
            box-shadow: 0 16px 32px rgba(31, 111, 120, 0.22);
            transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 18px 36px rgba(31, 111, 120, 0.26);
            filter: brightness(1.02);
        }

        .stButton > button:focus {
            outline: 3px solid rgba(31, 111, 120, 0.16);
            outline-offset: 2px;
        }

        .result-panel.high {
            background: linear-gradient(180deg, #fffdfa 0%, var(--warn-soft) 100%);
            border-color: #f0d8ca;
        }

        .result-panel.low {
            background: linear-gradient(180deg, #fcfffe 0%, var(--ok-soft) 100%);
            border-color: #d6ecdf;
        }

        .result-badge {
            display: inline-block;
            padding: 0.4rem 0.75rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 0.8rem;
        }

        .high .result-badge {
            background: rgba(166, 93, 52, 0.10);
            color: var(--warn);
        }

        .low .result-badge {
            background: rgba(34, 121, 93, 0.10);
            color: var(--ok);
        }

        .result-title {
            margin: 0;
            font-size: 1.6rem;
            line-height: 1.15;
            font-weight: 800;
        }

        .high .result-title {
            color: var(--warn);
        }

        .low .result-title {
            color: var(--ok);
        }

        .result-copy {
            margin: 0.7rem 0 0;
            color: var(--muted);
            font-size: 1rem;
            line-height: 1.75;
        }

        .stCaption {
            color: var(--muted);
            font-size: 0.93rem;
        }

        @media (max-width: 900px) {
            .topbar {
                flex-direction: column;
                align-items: flex-start;
            }

            .hero-panel {
                padding: 1.5rem;
            }

            .hero-grid {
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
            <section class="result-panel high">
                <div class="result-badge">Screening Result</div>
                <h2 class="result-title">Higher risk pattern detected</h2>
                <p class="result-copy">
                    The entered information matches a pattern this model associates with a higher
                    likelihood of heart disease. The profile includes a <strong>{sex.lower()}</strong>
                    patient, chest pain type <strong>{chest_pain.lower()}</strong>, and exercise-induced
                    angina marked <strong>{exercise_angina.lower()}</strong>. Please use this as supportive
                    screening information and follow it with proper clinical review.
                </p>
            </section>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <section class="result-panel low">
                <div class="result-badge">Screening Result</div>
                <h2 class="result-title">Lower risk pattern detected</h2>
                <p class="result-copy">
                    The entered information matches a pattern this model associates with a lower
                    likelihood of heart disease. The profile includes a <strong>{sex.lower()}</strong>
                    patient, chest pain type <strong>{chest_pain.lower()}</strong>, and exercise-induced
                    angina marked <strong>{exercise_angina.lower()}</strong>. Medical judgment and formal
                    testing should still guide final decisions.
                </p>
            </section>
            """,
            unsafe_allow_html=True,
        )


inject_styles()
model, model_columns = load_assets()

st.markdown('<div class="app-shell">', unsafe_allow_html=True)

st.markdown(
    """
    <section class="topbar">
        <div class="brand-wrap">
            <div class="brand-mark">CI</div>
            <div>
                <h1 class="brand-title">CardioInsight</h1>
                <p class="brand-copy">Heart disease screening support with a clearer, easier interface.</p>
            </div>
        </div>
        <div class="topbar-badge">Designed For Everyday Use</div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero-panel">
        <div class="eyebrow">Heart Risk Assessment</div>
        <h2 class="hero-title">Simple to understand. Professional to present.</h2>
        <p class="hero-copy">
            This version is rebuilt to feel like a real healthcare app instead of a rough demo.
            It uses a cleaner structure, clearer labels, better spacing, and a guided form so
            patients, students, and reviewers can all use it more comfortably.
        </p>
        <div class="hero-grid">
            <div class="hero-stat">
                <span class="hero-stat-label">User Experience</span>
                <span class="hero-stat-value">Clearer layout with less visual clutter</span>
            </div>
            <div class="hero-stat">
                <span class="hero-stat-label">Accessibility</span>
                <span class="hero-stat-value">Softer colors and easier scanning</span>
            </div>
            <div class="hero-stat">
                <span class="hero-stat-label">Purpose</span>
                <span class="hero-stat-value">AI-assisted screening, not diagnosis</span>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

main_col, side_col = st.columns([1.55, 0.9], gap="large")

with main_col:
    st.markdown(
        """
        <section class="section-panel">
            <div class="section-kicker">Patient Information</div>
            <h3 class="section-title">Complete the screening form</h3>
            <p class="section-copy">
                Start with the basic patient details below. Each field is labeled in plain language
                to make the process easier for everyone using the page.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    col_one, col_two = st.columns(2, gap="large")

    with col_one:
        age = st.number_input("Age", min_value=1, max_value=120, value=50)
        st.markdown('<div class="field-help">Patient age in years.</div>', unsafe_allow_html=True)

        trestbps = st.number_input("Resting Blood Pressure", min_value=50, max_value=250, value=120)
        st.markdown(
            '<div class="field-help">Measured blood pressure while the patient is at rest.</div>',
            unsafe_allow_html=True,
        )

        chol = st.number_input("Cholesterol", min_value=100, max_value=600, value=200)
        st.markdown(
            '<div class="field-help">Serum cholesterol level used by the trained model.</div>',
            unsafe_allow_html=True,
        )

        sex = st.selectbox("Sex", ["Male", "Female"])
        st.markdown('<div class="field-help">Select the patient sex used during training.</div>', unsafe_allow_html=True)

    with col_two:
        thalch = st.number_input("Maximum Heart Rate", min_value=50, max_value=220, value=150)
        st.markdown(
            '<div class="field-help">Highest recorded heart rate during evaluation.</div>',
            unsafe_allow_html=True,
        )

        oldpeak = st.number_input("ST Depression (Oldpeak)", min_value=0.0, max_value=10.0, value=1.0)
        st.markdown(
            '<div class="field-help">ST depression value measured relative to rest.</div>',
            unsafe_allow_html=True,
        )

        chest_pain = st.selectbox(
            "Chest Pain Type",
            ["Asymptomatic", "Atypical Angina", "Non-Anginal Pain", "Typical Angina"],
        )
        st.markdown(
            '<div class="field-help">Choose the chest pain category that best matches the patient.</div>',
            unsafe_allow_html=True,
        )

        exercise_angina = st.selectbox("Exercise-Induced Angina", ["No", "Yes"])
        st.markdown(
            '<div class="field-help">Indicates whether angina appears during exercise.</div>',
            unsafe_allow_html=True,
        )

    st.caption(
        "This tool provides screening support only. It should always be used alongside medical judgment."
    )
    analyze = st.button("Analyze Patient Risk")

with side_col:
    st.markdown(
        """
        <section class="side-panel">
            <div class="section-kicker">How To Use</div>
            <h3 class="section-title">Three simple steps</h3>
            <div class="step-card">
                <div class="step-number">1</div>
                <h4 class="step-title">Enter the patient values</h4>
                <p class="step-copy">Fill in the available clinical details using the form on the left.</p>
            </div>
            <div class="step-card">
                <div class="step-number">2</div>
                <h4 class="step-title">Run the screening</h4>
                <p class="step-copy">Select the analysis button to generate a model-based result.</p>
            </div>
            <div class="step-card">
                <div class="step-number">3</div>
                <h4 class="step-title">Review the outcome</h4>
                <p class="step-copy">Use the result as guidance, then confirm with proper medical evaluation.</p>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <section class="side-panel">
            <div class="section-kicker">What The Model Uses</div>
            <h3 class="section-title">Included inputs</h3>
            <p class="section-copy">
                Age, resting blood pressure, cholesterol, maximum heart rate, ST depression,
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

st.markdown("</div>", unsafe_allow_html=True)
