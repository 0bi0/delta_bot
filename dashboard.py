from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

SETTINGS_PATH = 'settings.json'

# Load settings from file
def load_settings():
    if not os.path.exists(SETTINGS_PATH):
        return {
            "anti_nuke": True,
            "anti_raid": True,
            "filter_system": True,
            "role_protection": True,
            "dangerous_permission_preventer": True,
            "webhook_deleter": True,
            "revenge_on_bot_remover": True
        }
    with open(SETTINGS_PATH, 'r') as f:
        return json.load(f)

# Save settings to file
def save_settings(settings):
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=2)

@app.route('/')
def index():
    settings = load_settings()
    return render_template('dashboard.html', settings=settings)

@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    save_settings(data)
    return jsonify({"status": "success"})

@app.route('/toggle', methods=['POST'])
def toggle():
    data = request.get_json()
    settings = load_settings()
    settings[data['feature']] = data['value']
    save_settings(settings)
    return jsonify({"status": "toggled"})
