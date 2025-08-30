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
        supervisor \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Don't hardcode PORT, let Render inject it
EXPOSE 10000

# Start all services with supervisord
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
