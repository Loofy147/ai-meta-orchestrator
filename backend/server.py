from flask import Flask, request, jsonify
import mlflow
import numpy as np
import os
import random

app = Flask(__name__)

# Set the MLflow tracking URI
mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "http://mlflow:5000"))

# Load models for A/B testing
model_a = mlflow.pyfunc.load_model(model_uri=f"models:/iris-model/1")
model_b = mlflow.pyfunc.load_model(model_uri=f"models:/iris-model/2")

@app.route("/")
def hello():
    return {"message": "Hello from the backend!"}

@app.route("/predict", methods=["POST"])
def predict():
    """
    Predicts the iris class.
    This endpoint performs A/B testing between two model versions.
    50% of the traffic goes to model A, and 50% to model B.
    """
    data = request.get_json(force=True)
    features = np.array(data['features']).reshape(1, -1)

    if random.random() < 0.5:
        prediction = model_a.predict(features)
        model_version = "A"
    else:
        prediction = model_b.predict(features)
        model_version = "B"

    return jsonify({
        "prediction": int(prediction[0]),
        "model_version": model_version
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
