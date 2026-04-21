import pickle
from typing import Any

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="CardioInsight | Heart Risk Screening",
    page_icon="H",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&display=swap');

        :root {
            --bg: #0b1220;
            --panel: #111a2b;
            --panel-soft: #162238;
            --panel-strong: #1b2b46;
            --line: rgba(255, 255, 255, 0.08);
            --text: #e7edf7;
            --muted: #9fb0cb;
            --accent: #4cc9f0;
            --accent-strong: #3a86ff;
            --success: #28c76f;
            --danger: #ff6b6b;
            --warning: #f4b740;
            --shadow: 0 22px 60px rgba(0, 0, 0, 0.28);
            --radius-lg: 26px;
            --radius-md: 18px;
            --radius-sm: 12px;
        }

        html, body, [class*="css"] {
            font-family: 'Manrope', system-ui, sans-serif;
            color: var(--text);
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(76, 201, 240, 0.12), transparent 28%),
                radial-gradient(circle at bottom right, rgba(58, 134, 255, 0.10), transparent 24%),
                linear-gradient(180deg, #08101c 0%, #0b1220 100%);
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 1.25rem;
            padding-bottom: 3rem;
        }

        .shell {
            background: rgba(10, 17, 30, 0.72);
            border: 1px solid var(--line);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow);
            backdrop-filter: blur(14px);
        }

        .hero-shell {
            padding: 1.75rem;
            margin-bottom: 1.2rem;
        }

        .hero-top {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            align-items: center;
            margin-bottom: 1.4rem;
        }

        .brand {
            display: flex;
            gap: 0.9rem;
            align-items: center;
        }

        .brand-mark {
            width: 52px;
            height: 52px;
            border-radius: 16px;
            display: grid;
            place-items: center;
            background: linear-gradient(135deg, #4cc9f0 0%, #3a86ff 100%);
            color: white;
            font-size: 1.15rem;
            font-weight: 800;
            letter-spacing: 0.08em;
        }

        .brand-name {
            font-size: 1.18rem;
            font-weight: 800;
            margin: 0;
        }

        .brand-copy {
            color: var(--muted);
            margin: 0.15rem 0 0;
            font-size: 0.92rem;
        }

        .eyebrow {
            display: inline-flex;
            padding: 0.38rem 0.7rem;
            border-radius: 999px;
            background: rgba(76, 201, 240, 0.12);
            border: 1px solid rgba(76, 201, 240, 0.18);
            color: #8de7ff;
            font-size: 0.74rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .hero-grid {
            display: grid;
            grid-template-columns: 1.2fr 0.9fr;
            gap: 1.2rem;
            align-items: stretch;
        }

        .hero-copy h1 {
            margin: 0.7rem 0 0.75rem;
            font-size: clamp(2rem, 5vw, 3.35rem);
            line-height: 1.02;
            letter-spacing: -0.04em;
        }

        .hero-copy p {
            margin: 0;
            max-width: 60ch;
            color: var(--muted);
            line-height: 1.8;
            font-size: 1rem;
        }

        .hero-badges {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.8rem;
            margin-top: 1.4rem;
        }

        .hero-badge {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--line);
            border-radius: var(--radius-md);
            padding: 0.95rem 1rem;
        }

        .hero-badge-title {
            font-size: 0.88rem;
            font-weight: 700;
            margin: 0 0 0.2rem;
        }

        .hero-badge-copy {
            margin: 0;
            color: var(--muted);
            font-size: 0.82rem;
            line-height: 1.55;
        }

        .notice-card {
            background: linear-gradient(180deg, rgba(255, 107, 107, 0.12), rgba(244, 183, 64, 0.08));
            border: 1px solid rgba(255, 107, 107, 0.20);
            border-radius: var(--radius-lg);
            padding: 1.3rem 1.35rem;
        }

        .notice-card h3 {
            margin: 0 0 0.5rem;
            font-size: 1.02rem;
            color: #ffd2d2;
        }

        .notice-card p {
            margin: 0;
            color: #ffdede;
            line-height: 1.7;
            font-size: 0.9rem;
        }

        .panel-title {
            margin: 0 0 0.3rem;
            font-size: 1.12rem;
            font-weight: 800;
            letter-spacing: -0.02em;
        }

        .panel-copy {
            margin: 0;
            color: var(--muted);
            line-height: 1.7;
            font-size: 0.92rem;
        }

        .section-shell {
            padding: 1.3rem 1.35rem;
            margin-bottom: 1rem;
        }

        .micro-label {
            color: #8de7ff;
            text-transform: uppercase;
            font-size: 0.72rem;
            letter-spacing: 0.08em;
            font-weight: 700;
            margin-bottom: 0.6rem;
        }

        .field-note {
            font-size: 0.8rem;
            color: var(--muted);
            margin-top: -0.2rem;
            margin-bottom: 0.55rem;
        }

        .stNumberInput label,
        .stSelectbox label {
            color: var(--text) !important;
            font-weight: 700 !important;
        }

        .stNumberInput [data-baseweb="input"],
        .stSelectbox [data-baseweb="select"] > div {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid var(--line) !important;
            border-radius: var(--radius-sm) !important;
            min-height: 2.9rem;
            color: var(--text) !important;
        }

        .stNumberInput [data-baseweb="input"]:focus-within,
        .stSelectbox [data-baseweb="select"] > div:focus-within {
            border-color: rgba(76, 201, 240, 0.42) !important;
            box-shadow: 0 0 0 3px rgba(76, 201, 240, 0.14) !important;
        }

        .stForm {
            border: none !important;
            padding: 0 !important;
        }

        .stButton > button,
        div[data-testid="stFormSubmitButton"] > button {
            width: 100%;
            border: none;
            border-radius: 16px;
            min-height: 3.2rem;
            background: linear-gradient(135deg, #4cc9f0 0%, #3a86ff 100%);
            color: white;
            font-size: 1rem;
            font-weight: 800;
            box-shadow: 0 18px 36px rgba(58, 134, 255, 0.26);
        }

        .stButton > button:hover,
        div[data-testid="stFormSubmitButton"] > button:hover {
            filter: brightness(1.04);
        }

        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--line);
            border-radius: 16px;
            padding: 0.95rem 1rem;
        }

        div[data-testid="stMetricLabel"] {
            color: var(--muted);
        }

        div[data-testid="stAlert"] {
            border-radius: 18px;
        }

        .side-list {
            display: grid;
            gap: 0.8rem;
            margin-top: 1rem;
        }

        .side-item {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--line);
            border-radius: 16px;
            padding: 1rem;
        }

        .side-item h4 {
            margin: 0 0 0.3rem;
            font-size: 0.94rem;
        }

        .side-item p {
            margin: 0;
            color: var(--muted);
            font-size: 0.84rem;
            line-height: 1.6;
        }

        .footer-note {
            text-align: center;
            color: var(--muted);
            font-size: 0.84rem;
            line-height: 1.8;
            padding: 1.25rem 0 0.4rem;
        }

        @media (max-width: 900px) {
            .hero-grid {
                grid-template-columns: 1fr;
            }

            .hero-badges {
                grid-template-columns: 1fr;
            }

            .hero-top {
                flex-direction: column;
                align-items: flex-start;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def inject_accessibility_fixes() -> None:
    components.html(
        """
        <script>
        const fixFormFields = () => {
          const doc = window.parent.document;
          const fieldConfigs = [
            { testid: "stNumberInput", selector: "input", prefix: "cardio-number" },
            { testid: "stSelectbox", selector: "[role='combobox']", prefix: "cardio-select" },
          ];

          fieldConfigs.forEach(({ testid, selector, prefix }) => {
            const wrappers = doc.querySelectorAll(`[data-testid="${testid}"]`);
            wrappers.forEach((wrapper, index) => {
              const field = wrapper.querySelector(selector);
              const label = wrapper.querySelector("label");
              if (!field) {
                return;
              }

              const fieldId = `${prefix}-${index + 1}`;
              field.id = fieldId;
              field.setAttribute("name", fieldId);
              if (label) {
                label.setAttribute("for", fieldId);
              }
            });
          });
        };

        fixFormFields();
        new MutationObserver(fixFormFields).observe(window.parent.document.body, {
          childList: true,
          subtree: true,
        });
        </script>
        """,
        height=0,
    )


@st.cache_resource(show_spinner=False)
def load_assets() -> tuple[Any, list[str]]:
    with open("heart_disease_model.pkl", "rb") as file:
        model = pickle.load(file)

    with open("model_columns.pkl", "rb") as file:
        model_columns = pickle.load(file)

    return model, model_columns


def build_input_frame(
    model_columns: list[str],
    age: int,
    trestbps: int,
    chol: int,
    thalch: int,
    oldpeak: float,
    sex: str,
    chest_pain: str,
    exercise_angina: str,
) -> pd.DataFrame:
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


def get_prediction_details(model: Any, input_data: pd.DataFrame) -> tuple[int, float | None]:
    prediction = int(model.predict(input_data)[0])
    probability = None
    if hasattr(model, "predict_proba"):
        probability = float(model.predict_proba(input_data)[0][1])
    return prediction, probability


def store_analysis_result(
    prediction: int,
    probability: float | None,
    sex: str,
    chest_pain: str,
    exercise_angina: str,
    age: int,
    trestbps: int,
    chol: int,
    thalch: int,
    oldpeak: float,
) -> None:
    st.session_state["analysis_result"] = {
        "prediction": prediction,
        "probability": probability,
        "sex": sex,
        "chest_pain": chest_pain,
        "exercise_angina": exercise_angina,
        "age": age,
        "trestbps": trestbps,
        "chol": chol,
        "thalch": thalch,
        "oldpeak": oldpeak,
    }


def render_hero() -> None:
    st.markdown(
        """
        <section class="shell hero-shell">
            <div class="hero-top">
                <div class="brand">
                    <div class="brand-mark">CI</div>
                    <div>
                        <p class="brand-name">CardioInsight</p>
                        <p class="brand-copy">AI-assisted heart risk screening</p>
                    </div>
                </div>
                <div class="eyebrow">Educational tool only</div>
            </div>
            <div class="hero-grid">
                <div class="hero-copy">
                    <div class="eyebrow">Heart risk assessment</div>
                    <h1>Professional screening experience with a clear, trustworthy result.</h1>
                    <p>
                        Enter a small set of clinical values and receive a clean screening summary.
                        This app is designed to feel simple for users and dependable on repeated
                        submissions, while keeping the medical disclaimer visible at all times.
                    </p>
                    <div class="hero-badges">
                        <div class="hero-badge">
                            <p class="hero-badge-title">Fast workflow</p>
                            <p class="hero-badge-copy">One focused form, one result panel, no hidden steps.</p>
                        </div>
                        <div class="hero-badge">
                            <p class="hero-badge-title">Reliable updates</p>
                            <p class="hero-badge-copy">Every press of Analyze refreshes the latest prediction.</p>
                        </div>
                        <div class="hero-badge">
                            <p class="hero-badge-title">Clear presentation</p>
                            <p class="hero-badge-copy">Result metrics, clinical context, and a medical warning.</p>
                        </div>
                    </div>
                </div>
                <div class="notice-card">
                    <h3>Important medical notice</h3>
                    <p>
                        This application is an educational machine learning demo. It is not a
                        medical device, does not replace a doctor, and must not be used as the
                        only basis for diagnosis or treatment decisions.
                    </p>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    st.markdown(
        """
        <section class="shell section-shell">
            <div class="micro-label">Process</div>
            <h3 class="panel-title">How this screening works</h3>
            <p class="panel-copy">
                The model uses a compact clinical profile and returns a binary screening output.
            </p>
            <div class="side-list">
                <div class="side-item">
                    <h4>1. Enter the patient profile</h4>
                    <p>Use age, blood pressure, cholesterol, max heart rate, ECG oldpeak, sex, chest pain, and exercise angina.</p>
                </div>
                <div class="side-item">
                    <h4>2. Submit the form</h4>
                    <p>Analyze runs the latest values and updates the result panel immediately on every press.</p>
                </div>
                <div class="side-item">
                    <h4>3. Review the output</h4>
                    <p>Read the risk label, summary metrics, and reminder to seek proper clinical evaluation.</p>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <section class="shell section-shell">
            <div class="micro-label">Model</div>
            <h3 class="panel-title">Model snapshot</h3>
            <p class="panel-copy">
                Dataset: Cleveland heart disease data. Output: screening classification.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_result_dashboard(result: dict[str, Any]) -> None:
    is_high_risk = result["prediction"] == 1
    heading = "Higher risk pattern detected" if is_high_risk else "Lower risk pattern detected"
    tone_fn = st.error if is_high_risk else st.success
    tone_icon = "🚨" if is_high_risk else "✅"

    st.markdown(
        """
        <section class="shell section-shell">
            <div class="micro-label">Latest result</div>
            <h3 class="panel-title">Screening summary</h3>
            <p class="panel-copy">This panel always reflects the most recent successful Analyze action.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    tone_fn(heading, icon=tone_icon)

    st.write(
        "Based on the submitted values, the model identified a pattern associated with a "
        f"**{'higher' if is_high_risk else 'lower'} likelihood** of heart disease."
    )

    top_metrics = st.columns(4)
    top_metrics[0].metric("Sex", result["sex"])
    top_metrics[1].metric("Chest pain", result["chest_pain"])
    top_metrics[2].metric("Exercise angina", result["exercise_angina"])
    top_metrics[3].metric("Age", str(result["age"]))

    lower_metrics = st.columns(4)
    lower_metrics[0].metric("Resting BP", f"{result['trestbps']} mm Hg")
    lower_metrics[1].metric("Cholesterol", f"{result['chol']} mg/dL")
    lower_metrics[2].metric("Max heart rate", str(result["thalch"]))
    lower_metrics[3].metric("Oldpeak", f"{result['oldpeak']:.1f}")

    probability = result["probability"]
    if probability is not None:
        st.progress(probability, text=f"Positive-class model score: {probability * 100:.1f}%")

    summary_col, action_col = st.columns([1.25, 0.95], gap="large")
    with summary_col:
        st.info(
            "This is a screening output, not a diagnosis. The score can support awareness and "
            "discussion, but it should never replace clinician judgment.",
            icon="ℹ",
        )
    with action_col:
        st.warning(
            "Recommended next step: discuss symptoms, history, and formal testing with a qualified healthcare professional.",
            icon="⚠️",
        )


def render_form(model: Any, model_columns: list[str]) -> None:
    st.markdown(
        """
        <section class="shell section-shell">
            <div class="micro-label">Assessment form</div>
            <h3 class="panel-title">Enter patient information</h3>
            <p class="panel-copy">
                Use the form below and press Analyze to generate a fresh result from the current values.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    with st.form("heart_risk_form", clear_on_submit=False):
        st.markdown('<div class="micro-label">Basic information</div>', unsafe_allow_html=True)
        basic_left, basic_right = st.columns(2, gap="medium")

        with basic_left:
            age = st.number_input("Age (years)", min_value=1, max_value=120, value=50)
            st.markdown('<div class="field-note">Patient age in years.</div>', unsafe_allow_html=True)

            sex = st.selectbox("Biological sex", ["Male", "Female"])
            st.markdown('<div class="field-note">Used exactly as encoded in the training data.</div>', unsafe_allow_html=True)

        with basic_right:
            chest_pain = st.selectbox(
                "Chest pain type",
                ["Asymptomatic", "Atypical Angina", "Non-Anginal Pain", "Typical Angina"],
            )
            st.markdown('<div class="field-note">Select the best clinical description.</div>', unsafe_allow_html=True)

            exercise_angina = st.selectbox("Exercise-induced angina", ["No", "Yes"])
            st.markdown('<div class="field-note">Indicates chest pain triggered by exercise.</div>', unsafe_allow_html=True)

        st.markdown('<div class="micro-label">Clinical measurements</div>', unsafe_allow_html=True)
        clinical_left, clinical_right = st.columns(2, gap="medium")

        with clinical_left:
            trestbps = st.number_input(
                "Resting blood pressure (mm Hg)",
                min_value=50,
                max_value=250,
                value=120,
            )
            st.markdown('<div class="field-note">Resting blood pressure recorded in mm Hg.</div>', unsafe_allow_html=True)

            chol = st.number_input(
                "Cholesterol (mg/dL)",
                min_value=100,
                max_value=600,
                value=200,
            )
            st.markdown('<div class="field-note">Total serum cholesterol value.</div>', unsafe_allow_html=True)

        with clinical_right:
            thalch = st.number_input(
                "Maximum heart rate achieved",
                min_value=50,
                max_value=220,
                value=150,
            )
            st.markdown('<div class="field-note">Peak heart rate during exercise testing.</div>', unsafe_allow_html=True)

            oldpeak = st.number_input(
                "ST depression (oldpeak)",
                min_value=0.0,
                max_value=10.0,
                value=1.0,
                step=0.1,
            )
            st.markdown('<div class="field-note">Exercise-induced ST depression relative to rest.</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("Analyze Heart Risk")

    if submitted:
        try:
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
            prediction, probability = get_prediction_details(model, input_data)
            store_analysis_result(
                prediction=prediction,
                probability=probability,
                sex=sex,
                chest_pain=chest_pain,
                exercise_angina=exercise_angina,
                age=age,
                trestbps=trestbps,
                chol=chol,
                thalch=thalch,
                oldpeak=oldpeak,
            )
            st.session_state["analysis_error"] = None
        except Exception as error:
            st.session_state["analysis_error"] = str(error)


def main() -> None:
    inject_styles()
    inject_accessibility_fixes()
    model, model_columns = load_assets()

    if "analysis_result" not in st.session_state:
        st.session_state["analysis_result"] = None
    if "analysis_error" not in st.session_state:
        st.session_state["analysis_error"] = None

    render_hero()

    form_col, sidebar_col = st.columns([1.65, 0.9], gap="large")

    with form_col:
        render_form(model, model_columns)

        if st.session_state["analysis_error"]:
            st.error(
                "The model could not generate a prediction from the submitted values.",
                icon="⚠️",
            )
            st.code(st.session_state["analysis_error"])
        elif st.session_state["analysis_result"] is not None:
            render_result_dashboard(st.session_state["analysis_result"])
        else:
            st.info(
                "No result yet. Complete the form and press Analyze Heart Risk to generate a screening summary.",
                icon="ℹ",
            )

    with sidebar_col:
        render_sidebar()

    st.markdown(
        """
        <div class="footer-note">
            CardioInsight is an educational AI screening application and not a medical device.
            Always seek professional medical advice for diagnosis, treatment, and urgent symptoms.
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
