from flask import Flask, render_template, request, redirect, url_for, flash
import os
import requests

app = Flask(__name__)
app.secret_key = "secret123"

GOOGLE_SHEET_WEBHOOK_URL = os.environ.get("GOOGLE_SHEET_WEBHOOK_URL")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    email = request.form.get("email")
    number = request.form.get("number")
    gender = request.form.get("gender")
    blood_group = request.form.get("bloodGroup")
    age = request.form.get("age")
    location = request.form.get("location")

    print("---- FORM DATA RECEIVED ----")
    print("request.form:", request.form)
    print("name:", name)
    print("email:", email)
    print("number:", number)
    print("gender:", gender)
    print("blood_group:", blood_group)
    print("age:", age)
    print("location:", location)

    data = {
        "name": name,
        "email": email,
        "number": number,
        "gender": gender,
        "blood_group": blood_group,
        "age": age,
        "location": location
    }

    print("---- JSON DATA TO SEND ----")
    print(data)

    try:
        if not GOOGLE_SHEET_WEBHOOK_URL:
            raise ValueError("GOOGLE_SHEET_WEBHOOK_URL is not set in environment variables")

        response = requests.post(GOOGLE_SHEET_WEBHOOK_URL, json=data, timeout=10)
        print("Webhook status:", response.status_code)
        print("Webhook response:", response.text)
        response.raise_for_status()
        flash("Registration successful and data saved.")
    except Exception as e:
        print("ERROR:", str(e))
        flash(f"Error saving registration: {str(e)}")

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
