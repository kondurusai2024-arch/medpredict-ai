from flask import Flask, render_template, request
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# =========================
# LOAD DATA
# =========================
heart_data = pd.read_csv("heart.csv")
thyroid_data = pd.read_csv("thyroid.csv")

heart_data.columns = heart_data.columns.str.strip()
thyroid_data.columns = thyroid_data.columns.str.strip()

# =========================
# HEART MODEL
# =========================
heart_X = heart_data.drop("target", axis=1)
heart_y = heart_data["target"]

heart_model = RandomForestClassifier(n_estimators=200, random_state=42)
heart_model.fit(heart_X, heart_y)

# =========================
# THYROID MODEL
# =========================
thyroid_X = thyroid_data.drop("target", axis=1)
thyroid_y = thyroid_data["target"]

thyroid_model = RandomForestClassifier(n_estimators=200, random_state=42)
thyroid_model.fit(thyroid_X, thyroid_y)

# =========================
# HEART TIPS
# =========================
def get_heart_advice(risk):
    if risk == "Low":
        tips = [
            "Your current heart condition appears to be in a safer range.",
            "Continue regular physical activity like walking or light exercise.",
            "Maintain a balanced diet with less oil and salt."
        ]
        precautions = [
            "Avoid frequent junk food and sugary drinks.",
            "Do yearly health checkups for BP, sugar, and cholesterol.",
            "Maintain good sleep and hydration."
        ]

    elif risk == "Moderate":
        tips = [
            "Your heart risk is moderate. Lifestyle improvement is advised.",
            "Reduce oily, fried, and processed foods.",
            "Exercise daily and monitor your BP regularly."
        ]
        precautions = [
            "Avoid smoking and alcohol.",
            "Control stress using yoga, breathing, or walking.",
            "Consult a doctor if you feel chest pain or breathlessness."
        ]

    else:
        tips = [
            "High heart risk detected. Please seek medical consultation soon.",
            "Follow a strict heart-friendly diet immediately.",
            "Monitor BP, sugar, and symptoms frequently."
        ]
        precautions = [
            "Do not ignore chest pain, dizziness, or shortness of breath.",
            "Avoid smoking, alcohol, and fatty foods completely.",
            "Follow all doctor advice and medical tests on time."
        ]

    return tips, precautions

# =========================
# THYROID TIPS
# =========================
def get_thyroid_advice(risk):
    if risk == "Low":
        tips = [
            "Your thyroid condition appears to be in a normal range.",
            "Maintain a healthy diet with proper iodine and nutrients.",
            "Regular exercise and sleep help hormone balance."
        ]
        precautions = [
            "Avoid taking thyroid medicine without doctor advice.",
            "Watch for sudden weight or energy changes.",
            "Do routine thyroid tests if recommended."
        ]

    elif risk == "Moderate":
        tips = [
            "Possible thyroid imbalance detected.",
            "Maintain regular food timings and healthy sleep.",
            "Track symptoms like fatigue, hair fall, and mood changes."
        ]
        precautions = [
            "Consult a doctor if symptoms continue.",
            "Repeat thyroid profile tests if needed.",
            "Reduce stress and improve daily routine."
        ]

    else:
        tips = [
            "High thyroid-related risk detected. Medical consultation is recommended.",
            "Proper thyroid testing and treatment may be needed.",
            "Follow a regular medicine, food, and sleep schedule."
        ]
        precautions = [
            "Do not ignore fatigue, swelling, or rapid weight changes.",
            "Take medicines only as prescribed.",
            "Regular testing and doctor follow-up are important."
        ]

    return tips, precautions

# =========================
# HOME
# =========================
@app.route("/")
def home():
    return render_template(
        "index.html",
        prediction_text=None,
        probability=None,
        risk_level=None,
        disease_type="heart",
        tips=[],
        precautions=[]
    )

# =========================
# SAFE FLOAT
# =========================
def safe_float(value, default=0):
    try:
        if value is None or value == "":
            return default
        return float(value)
    except:
        return default

# =========================
# PREDICT
# =========================
@app.route("/predict", methods=["POST"])
def predict():
    try:
        disease_type = request.form.get("disease_type", "heart")
        print("Selected Disease Type:", disease_type)

        # ================= HEART =================
        if disease_type == "heart":
            input_data = {
                "age": safe_float(request.form.get("age")),
                "sex": safe_float(request.form.get("sex")),
                "cp": safe_float(request.form.get("cp")),
                "trestbps": safe_float(request.form.get("trestbps")),
                "chol": safe_float(request.form.get("chol")),
                "fbs": safe_float(request.form.get("fbs")),
                "restecg": safe_float(request.form.get("restecg")),
                "thalach": safe_float(request.form.get("thalach")),
                "exang": safe_float(request.form.get("exang")),
                "oldpeak": safe_float(request.form.get("oldpeak")),
                "slope": safe_float(request.form.get("slope")),
                "ca": safe_float(request.form.get("ca")),
                "thal": safe_float(request.form.get("thal"))
            }

            input_df = pd.DataFrame([input_data])[heart_X.columns]

            prob = heart_model.predict_proba(input_df)[0][1] * 100

            # Better thresholds
            if prob < 40:
                disease = "No Heart Disease"
                risk = "Low"
            elif prob < 75:
                disease = "Possible Heart Risk"
                risk = "Moderate"
            else:
                disease = "Heart Disease Detected"
                risk = "High"

            tips, precautions = get_heart_advice(risk)

        # ================= THYROID =================
        else:
            input_data = {
                "age": safe_float(request.form.get("t_age")),
                "sex": safe_float(request.form.get("t_sex")),
                "tsh": safe_float(request.form.get("t_tsh")),
                "t3": safe_float(request.form.get("t_t3")),
                "tt4": safe_float(request.form.get("t_tt4")),
                "t4u": safe_float(request.form.get("t_t4u")),
                "fti": safe_float(request.form.get("t_fti"))
            }

            input_df = pd.DataFrame([input_data])[thyroid_X.columns]

            prob = thyroid_model.predict_proba(input_df)[0][1] * 100

            if prob < 40:
                disease = "No Thyroid Disease"
                risk = "Low"
            elif prob < 75:
                disease = "Possible Thyroid Risk"
                risk = "Moderate"
            else:
                disease = "Thyroid Disease Detected"
                risk = "High"

            tips, precautions = get_thyroid_advice(risk)

        print("Probability:", prob)
        print("Risk:", risk)

        return render_template(
            "index.html",
            prediction_text=f"{disease} ({risk} Risk)",
            probability=round(prob, 2),
            risk_level=risk,
            disease_type=disease_type,
            tips=tips,
            precautions=precautions
        )

    except Exception as e:
        print("ERROR:", e)
        return render_template(
            "index.html",
            prediction_text=f"Error: {str(e)}",
            probability=None,
            risk_level=None,
            disease_type="heart",
            tips=[],
            precautions=[]
        )

if __name__ == "__main__":
    app.run(debug=True)