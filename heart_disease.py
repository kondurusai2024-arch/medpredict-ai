from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# Load trained files
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
training_columns = pickle.load(open("columns.pkl", "rb"))

@app.route("/")
def home():
    return render_template(
        "index.html",
        prediction_text=None,
        probability=None,
        risk_level=None,
        tips=[],
        precautions=[]
    )

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Read user input
        row = {
            "age": float(request.form["age"]),
            "sex": int(request.form["sex"]),
            "cp": int(request.form["cp"]),
            "trestbps": float(request.form["trestbps"]),
            "chol": float(request.form["chol"]),
            "fbs": int(request.form["fbs"]),
            "restecg": int(request.form["restecg"]),
            "thalach": float(request.form["thalach"]),
            "exang": int(request.form["exang"]),
            "oldpeak": float(request.form["oldpeak"]),
            "slope": int(request.form["slope"]),
            "ca": int(request.form["ca"]),
            "thal": int(request.form["thal"])
        }

        # Convert to DataFrame
        input_df = pd.DataFrame([row])

        # Apply same encoding as training
        input_df = pd.get_dummies(input_df, columns=['cp', 'restecg', 'thal'], drop_first=True)

        # Match exact training columns
        input_df = input_df.reindex(columns=training_columns, fill_value=0)

        # Scale input
        scaled_input = scaler.transform(input_df)

        # Get probabilities
        probabilities = model.predict_proba(scaled_input)[0]

        # FIXED: use probabilities[0] instead of probabilities[1]
        disease_probability = round(probabilities[0] * 100, 2)

        # -----------------------------------
        # DEMO-FRIENDLY RESULT LOGIC
        # -----------------------------------
        if disease_probability >= 70:
            disease_status = "⚠️ Heart Disease Exists"
            risk_level = "High"

            tips = [
                "Consult a cardiologist immediately.",
                "Monitor BP, sugar, and cholesterol frequently.",
                "Follow a strict heart-healthy diet.",
                "Avoid smoking, alcohol, and stress."
            ]
            precautions = [
                "Do not ignore chest pain or shortness of breath.",
                "Seek urgent medical help if symptoms worsen.",
                "Follow doctor advice and regular check-ups."
            ]

        elif disease_probability >= 40:
            disease_status = "🟠 Heart Disease May Exist"
            risk_level = "Medium"

            tips = [
                "Reduce oily, salty, and processed food.",
                "Exercise or walk 30 minutes daily.",
                "Maintain proper sleep and reduce stress.",
                "Do regular health screening."
            ]
            precautions = [
                "Watch for unusual fatigue or chest discomfort.",
                "Maintain healthy weight.",
                "Reduce salt, sugar, and unhealthy fats."
            ]

        else:
            disease_status = "✅ No Heart Disease"
            risk_level = "Low"

            tips = [
                "Continue balanced diet and regular exercise.",
                "Maintain healthy sleep and hydration.",
                "Keep regular preventive health check-ups."
            ]
            precautions = [
                "Avoid smoking and junk food.",
                "Stay active and manage stress."
            ]

        prediction_text = f"{disease_status} ({risk_level} Risk)"

        return render_template(
            "index.html",
            prediction_text=prediction_text,
            probability=disease_probability,
            risk_level=risk_level,
            tips=tips,
            precautions=precautions
        )

    except Exception as e:
        return render_template(
            "index.html",
            prediction_text=f"Error: {str(e)}",
            probability=None,
            risk_level=None,
            tips=[],
            precautions=[]
        )

if __name__ == "__main__":
    app.run(debug=True)