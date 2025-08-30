
FROM python:3.10-slim
WORKDIR /app/auth_service
COPY . .
RUN pip install --no-cache-dir flask pyjwt
EXPOSE 6200
CMD ["python", "app.py"]
