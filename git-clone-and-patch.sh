
#!/bin/bash
set -e
echo "[*] This script will clone the required GitHub repos and apply adapter files so they run in Docker."
echo "[*] Make sure git is installed and you have network access."

ROOT_DIR="$(pwd)"

clone_or_skip() {
  local url=$1; local dir=$2
  if [ -d "$dir" ]; then
    echo "[*] Directory $dir already exists — skipping clone."
  else
    echo "[*] Cloning $url into $dir..."
    git clone "$url" "$dir" || { echo "Clone failed for $url"; exit 1; }
  fi
}

# Clone repos
clone_or_skip https://github.com/cowrie/cowrie.git cowrie
clone_or_skip https://github.com/melisasvr/AI-Powered-Cybersecurity-Threat-Detection-System.git "AI-Powered-Cybersecurity-Threat-Detection-System"
clone_or_skip https://github.com/rkalis/blockchain-audit-trail.git blockchain-audit-trail
clone_or_skip https://github.com/webpro255/network-anomaly-detection.git network-anomaly-detection

echo "[*] Applying adapter files (Dockerfiles/start scripts) into cloned repositories..."
cp -r adapters/cowrie/* cowrie/ 2>/dev/null || true
cp -r adapters/ai/* "AI-Powered-Cybersecurity-Threat-Detection-System/" 2>/dev/null || true
cp -r adapters/blockchain/* blockchain-audit-trail/ 2>/dev/null || true
cp -r adapters/dashboard/* network-anomaly-detection/ 2>/dev/null || true

echo "[*] Adapters applied. You can now run: docker-compose up --build"
