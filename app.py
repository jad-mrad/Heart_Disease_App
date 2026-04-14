import streamlit as st
import pandas as pd
import pickle

# 1. Load the model and columns
with open('heart_disease_model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('model_columns.pkl', 'rb') as file:
    model_columns = pickle.load(file)

# 2. Build the Website UI
st.title("🫀 AI Heart Disease Predictor")
st.write("Enter patient details to predict heart disease risk based on our Decision Tree model.")

st.header("Patient Vitals")
age = st.number_input("Age", min_value=1, max_value=120, value=50)
trestbps = st.number_input("Resting Blood Pressure", min_value=50, max_value=250, value=120)
chol = st.number_input("Cholesterol", min_value=100, max_value=600, value=200)
thalch = st.number_input("Maximum Heart Rate", min_value=50, max_value=220, value=150)
oldpeak = st.number_input("Oldpeak (ST depression)", min_value=0.0, max_value=10.0, value=1.0)
sex = st.selectbox("Sex", ["Male", "Female"])

# 3. Predict Button Logic
if st.button("Analyze Risk"):
    # Calculate our custom engineered features
    high_bp = 1 if trestbps > 130 else 0
    high_chol = 1 if chol > 240 else 0
    age_risk = age * oldpeak
    
    # Create a blank dataframe with the exact columns our model expects, filled with 0s
    input_data = pd.DataFrame(0, index=[0], columns=model_columns)
    
    # Fill in the data we know
    input_data['age'] = age
    input_data['trestbps'] = trestbps
    input_data['chol'] = chol
    input_data['thalch'] = thalch
    input_data['oldpeak'] = oldpeak
    input_data['High_BP'] = high_bp
    input_data['High_Chol'] = high_chol
    input_data['Age_Risk'] = age_risk
    
    # Handle the categorical dummy variable for sex
    if sex == 'Male' and 'sex_Male' in input_data.columns:
        input_data['sex_Male'] = 1
        
    # Make the prediction!
    prediction = model.predict(input_data)
    
    st.divider()
    if prediction[0] == 1:
        st.error("🚨 **High Risk:** The AI predicts Heart Disease. Please consult a doctor.")
    else:
        st.success("✅ **Low Risk:** The AI predicts No Heart Disease.")