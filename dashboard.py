from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route("/")
def index():
    with open("settings.json", "r") as f:
        settings = json.load(f)
    return render_template("dashboard.html", settings=settings)

@app.route("/save", methods=["POST"])
def save_settings():
    try:
        new_settings = request.get_json()
        print("[DEBUG] Received settings:", new_settings)
        with open("settings.json", "w") as f:
            json.dump(new_settings, f, indent=4)
        return jsonify({"success": True})
    except Exception as e:
        print("[ERROR]", e)
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
