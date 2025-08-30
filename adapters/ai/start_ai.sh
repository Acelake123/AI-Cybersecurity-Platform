#!/bin/bash
if [ -f run_server.py ]; then
  echo "Found run_server.py - executing it"
  python run_server.py
elif [ -f app.py ]; then
  echo "Found app.py - executing it"
  python app.py
else
  echo "No server found in AI repo - launching fallback predictor"
  python - <<'PY'
from flask import Flask, request, jsonify
app = Flask(__name__)
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json() or {}
    payload = str(data.get("payload","")).upper()
    score = 0.0
    for k in ["FAILED","NMAP","ROOT","ATTACK"]:
        if k in payload:
            score += 0.5
    if int(data.get("dst_port",0)) in (22,23):
        score += 0.2
    score=min(score,0.99)
    return jsonify({"score":score,"anomaly":score>=0.5})
if __name__=='__main__':
    app.run(host='0.0.0.0', port=6000)
PY
fi
