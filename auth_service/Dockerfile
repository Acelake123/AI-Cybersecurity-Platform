
FROM python:3.10-slim
WORKDIR /app
COPY auth_service /app/auth_service
RUN pip install --no-cache-dir flask pyjwt
EXPOSE 6200
CMD ["python", "auth_service/app.py"]
