FROM python:3.10-slim

# Install system dependencies for pycairo, reportlab, etc.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
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

# Use Render-assigned PORT environment variable
ENV PORT=7000
EXPOSE 7000

# Recommended for production: Use Gunicorn
RUN pip install gunicorn
CMD sh -c "gunicorn integration_server:app --bind 0.0.0.0:\$PORT --workers 2 --threads 4"

