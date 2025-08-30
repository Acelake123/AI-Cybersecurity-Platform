from flask import Flask, request, jsonify
import requests, os, sqlite3, json, time
from web3 import Web3

app = Flask(__name__)

# Internal service URLs (fixed local ports inside container)
AUTH_URL = os.getenv("AUTH_URL", "http://localhost:5001")
AI_URL = os.getenv("AI_URL", "http://localhost:5002/predict")
BLOCKCHAIN_URL = os.getenv("BLOCKCHAIN_URL", "http://localhost:5003")
MAPBOX_URL = os.getenv("MAPBOX_URL", "http://localhost:5004")
GANACHE = os.getenv("GANACHE_RPC", "http://localhost:8545")

# Database
DB_PATH = os.getenv("INTEGRATION_DB", "data/alerts.db")
PORT = int(os.getenv("PORT", 7000))  # Render injects PORT at runtime

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Initialize SQLite database
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS alerts
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      ts REAL,
                      src_ip TEXT,
                      dst_ip TEXT,
                      score REAL,
                      tx_hash TEXT,
                      raw TEXT)''')
        conn.commit()

init_db()

# Root route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Integration Server is running"}), 200

# Health check to verify subservices
@app.route('/health', methods=['GET'])
def health():
    status = {}
    for name, url in {
        "auth": AUTH_URL,
        "ai": AI_URL.replace("/predict", ""),
        "blockchain": BLOCKCHAIN_URL,
        "mapbox": MAPBOX_URL
    }.items():
        try:
            r = requests.get(url, timeout=3)
            status[name] = "ok" if r.status_code == 200 else f"error:{r.status_code}"
        except Exception as e:
            status[name] = f"down:{e}"
    return jsonify(status)

# Ingest route
@app.route('/ingest', methods=['POST'])
def ingest():
    payload = request.get_json()
    if not payload:
        return jsonify({"error": "invalid json"}), 400

    # Call AI service
    try:
        r = requests.post(AI_URL, json=payload, timeout=10)
        r.raise_for_status()
        ai_resp = r.json()
    except Exception as e:
        return jsonify({"error": "ai service failed", "details": str(e)}), 500

    score = float(ai_resp.get("score", 0.0))
    is_anomaly = ai_resp.get("anomaly", False)
    tx_hash = None

    # Record anomaly on blockchain if detected
    if is_anomaly:
        try:
            w3 = Web3(Web3.HTTPProvider(GANACHE))
            acct = w3.eth.accounts[0] if w3.eth.accounts else w3.eth.account.create().address
            data_hex = Web3.to_hex(text=json.dumps(payload).encode())
            tx = {"from": acct, "to": acct, "value": 0, "gas": 300000, "data": data_hex}
            tx_hash = w3.eth.send_transaction(tx).hex()
        except Exception as e:
            tx_hash = f"error:{e}"

    # Save alert in SQLite
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO alerts (ts, src_ip, dst_ip, score, tx_hash, raw) VALUES (?, ?, ?, ?, ?, ?)",
            (time.time(), payload.get("src_ip", ""), payload.get("dst_ip", ""), score, tx_hash or "", json.dumps(payload))
        )
        alert_id = c.lastrowid

    return jsonify({"id": alert_id, "anomaly": is_anomaly, "score": score, "tx_hash": tx_hash})

# Alerts route
@app.route('/alerts', methods=['GET'])
def alerts():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT id, ts, src_ip, dst_ip, score, tx_hash, raw FROM alerts ORDER BY id DESC LIMIT 500")
        rows = c.fetchall()
    out = [
        {"id": r[0], "ts": r[1], "src_ip": r[2], "dst_ip": r[3], "score": r[4], "tx_hash": r[5], "raw": json.loads(r[6])}
        for r in rows
    ]
    return jsonify(out)

# Only use app.run for local dev
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=False)
