
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt || true; fi
COPY start_ai.sh /start_ai.sh
RUN chmod +x /start_ai.sh
EXPOSE 6000
CMD ["/start_ai.sh"]
