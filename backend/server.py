from flask import Flask, request, jsonify
import mlflow
import numpy as np

app = Flask(__name__)

# Load the model from the MLflow model registry
model_name = "iris-model"
model_version = 1
model = mlflow.pyfunc.load_model(model_uri=f"models:/{model_name}/{model_version}")

@app.route("/")
def hello():
    return {"message": "Hello from the backend!"}

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)
    features = np.array(data['features']).reshape(1, -1)
    prediction = model.predict(features)
    return jsonify({"prediction": int(prediction[0])})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
