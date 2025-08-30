
# Adapter Dockerfile for cowrie repo
FROM python:3.10-slim
WORKDIR /app/adapters/cowrie
COPY . .
RUN pip install --no-cache-dir -r requirements.txt || true
CMD ["bin/cowrie", "start", "-n"]
# Use "-n" to run in the foreground for Docker