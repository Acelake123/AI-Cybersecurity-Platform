
FROM python:3.10-slim
WORKDIR /app/adapters/blockchain
COPY . .
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt || true; fi
CMD ["bash","-lc","if [ -f run_blockchain.py ]; then python run_blockchain.py; elif [ -f app.py ]; then python app.py; else echo 'No blockchain service entrypoint found'; tail -f /dev/null; fi"]
