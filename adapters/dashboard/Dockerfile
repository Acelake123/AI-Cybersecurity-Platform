
FROM node:18-alpine
WORKDIR /app
COPY . /app
RUN if [ -f package.json ]; then npm install --silent || true; fi
COPY start_dashboard.sh /start_dashboard.sh
RUN chmod +x /start_dashboard.sh
EXPOSE 5000
CMD ["/start_dashboard.sh"]
