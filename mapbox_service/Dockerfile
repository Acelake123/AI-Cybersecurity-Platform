FROM python:3.10-slim
WORKDIR /app/mapbox_service
COPY . .
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi
EXPOSE 6300
CMD ["python", "server.py"]
