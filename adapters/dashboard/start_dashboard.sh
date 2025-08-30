#!/bin/sh
if [ -f package.json ]; then
  if grep -q "\"start\"" package.json; then
    npm run start
  elif grep -q "\"dev\"" package.json; then
    npm run dev
  else
    if [ -d build ]; then
      npx http-server build -p 5000 || python -m http.server 5000
    else
      echo "No start script and no build; sleeping"
      tail -f /dev/null
    fi
  fi
else
  echo "No package.json - starting a simple Flask placeholder"
  python - <<'PY'
from flask import Flask, render_template_string
app = Flask(__name__)
@app.route('/')
def index():
    return "<h1>Network Anomaly Detection Dashboard (placeholder)</h1><p>Replace with real dashboard repo files.</p>"
app.run(host='0.0.0.0', port=5000)
PY
fi
