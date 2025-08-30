
FROM python:3.10-slim
WORKDIR /app
COPY mapbox_service /app/mapbox_service
RUN pip install --no-cache-dir flask requests
EXPOSE 6300
CMD ["python", "mapbox_service/app.py"]
