"""This module contains the Flask server for the MLOps demo."""
from flask import Flask, request, jsonify
import mlflow
import numpy as np

app = Flask(__name__)

# Load the model from the MLflow model registry
MODEL_NAME = "iris-model"
MODEL_VERSION = 1
model = mlflow.pyfunc.load_model(model_uri=f"models:/{MODEL_NAME}/{MODEL_VERSION}")

@app.route("/")
def hello():
    """Return a simple hello message."""
    return {"message": "Hello from the backend!"}

@app.route("/predict", methods=["POST"])
def predict():
    """Predict the class of an iris flower."""
    data = request.get_json(force=True)
    features = np.array(data['features']).reshape(1, -1)
    prediction = model.predict(features)
    return jsonify({"prediction": int(prediction[0])})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
