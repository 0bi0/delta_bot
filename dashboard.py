from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/save", methods=["POST"])
def save_settings():
    try:
        new_settings = request.get_json()
        with open(SETTINGS_FILE, "w") as f:
            json.dump(new_settings, f, indent=4)
        return jsonify({"success": True})
    except Exception as e:
        print(f"⚠️ Error saving settings: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
