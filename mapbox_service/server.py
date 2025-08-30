
from flask import Flask, render_template, jsonify
import os, requests, json
app = Flask(__name__, template_folder='templates')
INTEGRATION = os.getenv("INTEGRATION_URL", "http://integration_server:7000")
MAPBOX_KEY = os.getenv("MAPBOX_API_KEY", "")

@app.route('/map')
def map_page():
    return render_template("map.html", mapbox_key=MAPBOX_KEY)

@app.route('/data/alerts')
def alerts():
    try:
        r = requests.get(INTEGRATION + "/alerts", timeout=5)
        return jsonify(r.json())
    except Exception as e:
        return jsonify([])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6300)
