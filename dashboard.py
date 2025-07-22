from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

SETTINGS_FILE = "settings.json"

def get_settings():
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

@app.route("/")
def dashboard():
    return render_template("dashboard.html", settings=get_settings())


@app.route("/save", methods=["POST"])
def save_settings():
    try:
        settings = request.json
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
        return jsonify(success=True)
    except Exception as e:
        print(f"[ERROR] Failed to save settings: {e}")
        return jsonify(success=False, error=str(e)), 500


if __name__ == "__main__":
    app.run(debug=True)
