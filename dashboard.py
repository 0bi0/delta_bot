from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

SETTINGS_FILE = "settings.json"

@app.route("/")
def index():
    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)
    return render_template("dashboard.html", settings=settings)

@app.route("/save", methods=["POST"])
def save_settings():
    try:
        settings = request.json  # ← This is what the frontend sends
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=2)
        return jsonify({"status": "success"})
    except Exception as e:
        print("Save error:", e)
        return jsonify({"status": "error"}), 500
