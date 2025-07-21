from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

SETTINGS_FILE = "settings.json"

def load_settings():
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

@app.route("/", methods=["GET", "POST"])
def dashboard():
    settings = load_settings()
    if request.method == "POST":
        for key in settings:
            settings[key] = request.form.get(key) == "on"
        save_settings(settings)
        return redirect(url_for("dashboard"))
    return render_template("dashboard.html", settings=settings)

if __name__ == "__main__":
    app.run(debug=True, port=5000)