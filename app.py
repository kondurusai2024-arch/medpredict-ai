from flask import Flask, render_template, request

app = Flask(__name__)

# =====================================================
# SAFE FLOAT
# =====================================================
def safe_float(value, default=0):
    try:
        if value == "" or value is None:
            return default
        return float(value)
    except:
        return default


# =====================================================
# HEART ADVICE
# =====================================================
def get_heart_advice(risk):
    if risk == "Low":
        tips = [
            "Heart condition appears normal.",
            "Continue regular walking or exercise.",
            "Maintain healthy diet and sleep."
        ]
        precautions = [
            "Avoid junk food.",
            "Check BP yearly.",
            "Stay stress free."
        ]

    elif risk == "Moderate":
        tips = [
            "Some heart risk factors found.",
            "Reduce oily foods.",
            "Exercise daily."
        ]
        precautions = [
            "Monitor cholesterol.",
            "Reduce stress.",
            "Consult doctor if symptoms appear."
        ]

    else:
        tips = [
            "High heart risk detected.",
            "Consult cardiologist immediately.",
            "Follow strict diet."
        ]
        precautions = [
            "Do not ignore chest pain.",
            "Avoid smoking/alcohol.",
            "Take tests regularly."
        ]

    return tips, precautions


# =====================================================
# THYROID ADVICE
# =====================================================
def get_thyroid_advice(risk):
    if risk == "Low":
        tips = [
            "Thyroid values appear normal.",
            "Continue balanced diet.",
            "Exercise regularly."
        ]
        precautions = [
            "Do yearly thyroid checkup.",
            "Sleep well.",
            "Stay active."
        ]

    elif risk == "Moderate":
        tips = [
            "Possible thyroid imbalance.",
            "Retest thyroid profile.",
            "Maintain healthy weight."
        ]
        precautions = [
            "Watch fatigue or weight gain.",
            "Reduce stress.",
            "Consult doctor if symptoms continue."
        ]

    else:
        tips = [
            "High thyroid risk detected.",
            "Consult endocrinologist.",
            "Further thyroid tests needed."
        ]
        precautions = [
            "Do not ignore weakness.",
            "Take medicines only by doctor advice.",
            "Regular monitoring required."
        ]

    return tips, precautions


# =====================================================
# HOME
# =====================================================
@app.route("/")
def home():
    return render_template(
        "index.html",
        prediction_text=None,
        probability=None,
        risk_level=None,
        tips=[],
        precautions=[],
        disease_type="heart"
    )


# =====================================================
# PREDICT
# =====================================================
@app.route("/predict", methods=["POST"])
def predict():
    try:
        disease_type = request.form.get("disease_type", "heart")

        # =================================================
        # HEART PREDICTION
        # =================================================
        if disease_type == "heart":

            age = safe_float(request.form.get("age"))
            bp = safe_float(request.form.get("trestbps"))
            chol = safe_float(request.form.get("chol"))
            sugar = safe_float(request.form.get("fbs"))
            hr = safe_float(request.form.get("thalach"))
            angina = safe_float(request.form.get("exang"))
            oldpeak = safe_float(request.form.get("oldpeak"))
            ca = safe_float(request.form.get("ca"))

            score = 0

            if age > 55:
                score += 15
            elif age > 45:
                score += 8

            if bp > 140:
                score += 15
            elif bp > 125:
                score += 8

            if chol > 240:
                score += 15
            elif chol > 200:
                score += 8

            if sugar == 1:
                score += 10

            if hr < 130:
                score += 15
            elif hr < 160:
                score += 8

            if angina == 1:
                score += 15

            if oldpeak > 2:
                score += 10
            elif oldpeak > 1:
                score += 5

            if ca > 0:
                score += 10

            # MATCHING LABEL + PERCENTAGE
            if score < 20:
                risk = "Low"
                disease = "No Heart Disease"
                probability = 12 + (score * 0.8)

            elif score < 45:
                risk = "Moderate"
                disease = "Possible Heart Risk"
                probability = 35 + ((score - 20) * 1.0)

            else:
                risk = "High"
                disease = "Heart Disease Detected"
                probability = min(95, 65 + ((score - 45) * 0.8))

            tips, precautions = get_heart_advice(risk)

        # =================================================
        # THYROID PREDICTION
        # =================================================
        else:
            age = safe_float(request.form.get("age"))
            tsh = safe_float(request.form.get("t_tsh"))
            t3 = safe_float(request.form.get("t_t3"))
            tt4 = safe_float(request.form.get("t_tt4"))
            t4u = safe_float(request.form.get("t_t4u"))
            fti = safe_float(request.form.get("t_fti"))

            score = 0

            if tsh < 0.4 or tsh > 4.5:
                score += 30

            if t3 < 0.8 or t3 > 2.0:
                score += 20

            if tt4 < 70 or tt4 > 150:
                score += 20

            if t4u < 0.7 or t4u > 1.4:
                score += 15

            if fti < 80 or fti > 150:
                score += 15

            # MATCHING LABEL + PERCENTAGE
            if score < 20:
                risk = "Low"
                disease = "No Thyroid Disease"
                probability = 12 + (score * 0.8)

            elif score < 45:
                risk = "Moderate"
                disease = "Possible Thyroid Risk"
                probability = 35 + ((score - 20) * 1.0)

            else:
                risk = "High"
                disease = "Thyroid Disease Detected"
                probability = min(95, 65 + ((score - 45) * 0.8))

            tips, precautions = get_thyroid_advice(risk)

        return render_template(
            "index.html",
            prediction_text=f"{disease} ({risk} Risk)",
            probability=round(probability, 2),
            risk_level=risk,
            tips=tips,
            precautions=precautions,
            disease_type=disease_type
        )

    except Exception as e:
        return render_template(
            "index.html",
            prediction_text=f"Error: {str(e)}",
            probability=12,
            risk_level="Low",
            tips=[],
            precautions=[],
            disease_type="heart"
        )


# =====================================================
# RUN APP
# =====================================================
if __name__ == "__main__":
    app.run(debug=True)
