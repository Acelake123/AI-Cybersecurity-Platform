FROM python:3.10-slim

# Install system dependencies for pycairo, reportlab, etc.
RUN apt-get update && \
    apt-get install -y \
    gcc \
    build-essential \
    libcairo2-dev \
    pkg-config \
    python3-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7000
CMD ["python", "integration_server.py"]
