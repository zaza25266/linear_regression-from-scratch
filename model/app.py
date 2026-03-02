from flask import Flask, render_template, request, jsonify
import pandas as pd
from model import predict_cgpa

app = Flask(__name__)

EXCEL_FILE = "student_data.xlsx"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    student = [
        float(data["study_hours"]),
        float(data["attendance"]),
        float(data["consistency"]),
        float(data["self_study"]),
        float(data["sleep"]),
        float(data["stress"]),
        float(data["time_management"]),
        float(data["participation"]),
        float(data["screen_time"]),
        float(data["motivation"])
    ]

    predicted = predict_cgpa(student)

    return jsonify({
        "predicted_cgpa": predicted,
        "student": student
    })

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json

    student = data["student"]
    expected_cgpa = float(data["expected_cgpa"])

    df = pd.read_excel(EXCEL_FILE)

    new_row = student + [expected_cgpa]
    df.loc[len(df)] = new_row

    df.to_excel(EXCEL_FILE, index=False)

    return jsonify({"message": "Data saved successfully"})

if __name__ == "__main__":
    app.run(debug=True)
