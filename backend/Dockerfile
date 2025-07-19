FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# This is a simplified setup. In a real-world scenario, you would have
# a more sophisticated way to manage the ML lifecycle.
CMD python train.py && python detect_drift.py && python retrain.py && gunicorn -b 0.0.0.0:5000 server:app
