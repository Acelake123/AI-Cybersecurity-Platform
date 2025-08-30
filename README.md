
# AI Cybersecurity Platform - Ready Package (Real Repos + Adapters)

This package is prepared to run the real repositories inside Docker with pre-provided adapter files.
Because this environment cannot fetch GitHub, you must run the included script locally to clone and patch the repositories.

## Steps (one-time)
1. Unzip this package and `cd` into the folder.
2. Copy `.env.example` to `.env` and edit secrets (JWT_SECRET, MFA_SECRET_SEED, MAPBOX_API_KEY).
3. Run the clone-and-patch script (requires git):
   ```bash
   bash git-clone-and-patch.sh
   ```
   This will clone the following repos into the folder:
   - cowrie/cowrie -> ./cowrie
   - melisasvr/AI-Powered-Cybersecurity-Threat-Detection-System -> ./AI-Powered-Cybersecurity-Threat-Detection-System
   - rkalis/blockchain-audit-trail -> ./blockchain-audit-trail
   - webpro255/network-anomaly-detection -> ./network-anomaly-detection
   The script will then copy the adapter files from ./adapters into each repo so they can run under Docker.

4. Start the full system:
   ```bash
   docker-compose up --build
   ```

## Services
- Ganache (local blockchain): http://localhost:8545
- Integration server: http://localhost:7000 (alerts ingestion: /ingest, alerts list: /alerts)
- Dashboard: http://localhost:5000
- Auth service (MFA mock): http://localhost:6200
- Mapbox service (threat map): http://localhost:6300/map

## Notes & Troubleshooting
- Adapters copy files into repo folders. They will overwrite files with the same names in the repo (backup if needed).
- First `docker-compose up --build` will take time as Docker installs dependencies.
- If a repository already defines its own Dockerfile or start scripts, the adapter may be redundant but harmless.
- Mapbox demo uses randomized coords. Replace with GeoIP for production.
