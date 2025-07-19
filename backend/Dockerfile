FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Train the model, run drift detection, and retrain the model
RUN python model.py && python drift_detection.py && python retrain.py

CMD ["gunicorn", "-b", "0.0.0.0:5000", "server:app"]
